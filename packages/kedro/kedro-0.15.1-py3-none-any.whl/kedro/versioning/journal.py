# Copyright 2018-2019 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
#     or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module provides journal logging to enable versioning support for
Kedro project."""
import json
import logging
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Union

_JOURNAL_KEY = "kedro.journal"


class VersionJournal:
    """``VersionJournal`` class provides journal logging to enable versioning support for
    Kedro project.
    """

    def __init__(self, record_data: Dict[str, Any]):
        """Initialise ``VersionJournal`` as a session of the journal versioning,
        and log the project context with an unique identifier.

        Args:
            record_data: JSON serializable dictionary specific to project context.

        """
        self._id = str(uuid.uuid1())
        record_data["id"] = self._id
        record_data["git_sha"] = _git_sha(record_data["project_path"])
        self._log_journal("ContextJournalRecord", record_data)

    def _log_journal(self, record_type: str, record_data: Mapping) -> None:
        """Log a record to journal.

        Args:
            record_type: A unique type identifier.
            record_data: JSON serializable dictionary, specific to ``record_type``.

        """
        # pylint: disable=no-self-use
        try:
            logging.getLogger(_JOURNAL_KEY).info(
                json.dumps({"type": record_type, **record_data})
            )
        except TypeError:
            logging.getLogger(__name__).error(
                "Unable to record %s to journal, make sure it's a "
                "serializable dictionary",
                repr(record_data),
            )

    def log_catalog(
        self, dataset_name: str, operation: str, version: str = None
    ) -> None:
        """Log journal record for ``DataCatalog``.

        Args:
            dataset_name: Name of dataset being logged.
            operation: Operation on dataset, one of {'save', 'load'}.
            version: Dataset version corresponding to operation (i.e. if operation
                is 'save' then this is 'save_version').

        """
        record_data = {
            "id": self._id,
            "name": dataset_name,
            "operation": operation,
            "version": version,
        }
        self._log_journal("DatasetJournalRecord", record_data)


def _git_sha(proj_dir: Union[str, Path] = None) -> Optional[str]:
    """Git description of working tree.

    Returns: Git description or None.

    """
    proj_dir = str(proj_dir or Path.cwd())
    try:
        res = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=proj_dir
        )
        return res.decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.getLogger(__name__).warning("Unable to git describe %s", proj_dir)
    return None


class JournalFileHandler(logging.Handler):
    """Handler for logging journal record to a file based on journal ID.
    """

    def __init__(self, base_dir: Union[str, Path]):
        """Initialise ``JournalFileHandler`` which will handle logging journal record.

        Args:
            base_dir: Base directory for saving journals.

        """
        super(JournalFileHandler, self).__init__()
        self.base_dir = Path(base_dir).expanduser().resolve()
        self._file_handler_paths = {}  # type:Dict[str, Path]

    def _generate_log(self, journal_id) -> Path:
        """Generate unique filename for journal record path.

        Returns:
            Path to the journal log.

        """
        current_ts = datetime.now(tz=timezone.utc)
        fmt = (
            "{d.year:04d}-{d.month:02d}-{d.day:02d}T{d.hour:02d}"
            ".{d.minute:02d}.{d.second:02d}.{ms:03d}Z"
        )
        current_ts_str = fmt.format(d=current_ts, ms=current_ts.microsecond // 1000)
        return self.base_dir / ("journal_" + journal_id + current_ts_str + ".log")

    def emit(self, record: logging.LogRecord) -> None:
        """Overriding emit function in logging.Handler, which will output the record to
        the filelog based on journal id.

        Args:
            record: logging record.

        """
        message = json.loads(record.getMessage())

        handler_path = self._file_handler_paths.setdefault(
            message["id"], self._generate_log(message["id"])
        )

        handler_path.parent.mkdir(parents=True, exist_ok=True)
        logging.FileHandler(str(handler_path), mode="a").emit(record)
