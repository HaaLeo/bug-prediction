# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------


from collections import Counter
from os import path
import re

import git

# Used to determine different burst time periods.
BURST_PERIOD_THRESHOLD = 2 * 60**2  # 2 hours


class SourceControllManager(object): # pylint:disable=useless-object-inheritance

    def __init__(self, project_path):
        if path.isabs(project_path):
            self.__repository = git.Repo(project_path)
        else:
            self.__repository = git.Repo(path.abspath(project_path))

    def iter_change_periods(self, file_pattern):
        """
        Get the change count of each file per period.
        Time periods are determined dynamically as "burst time periods" (See the paper for further information).
        """

        period = {}

        # Starts with latest commit
        for commit in self.__repository.iter_commits():

            # For first iteration
            if not period:
                period = self.__init_period(commit.committed_date, commit.committed_datetime)

            # If within BURST_PERIOD_THRESHOLD seconds no code change occurred,
            # create a new time period
            if period['start_time']['epoch'] - BURST_PERIOD_THRESHOLD >= commit.committed_date:
                # yield period when it is finished
                yield period

                # Initialize new period
                period = self.__init_period(commit.committed_date, commit.committed_datetime)

            changes = self.__get_changes_for_commit(commit, file_pattern)

            # Sum changes per file
            period['changes'] += changes

            # Update period start time
            period['start_time']['epoch'] = commit.committed_date
            period['start_time']['datetime'] = commit.committed_datetime

        # Always yield last period so no commit is forgotten
        yield period

    @staticmethod
    def __get_changes_for_commit(commit, file_pattern):
        changes = {
            file_name:
                commit.stats.files[file_name].get('insertions', 0)
                + commit.stats.files[file_name].get('deletions', 0)
            for file_name in commit.stats.files
            if re.match(file_pattern, file_name)
        }

        return Counter(changes)

    @staticmethod
    def __init_period(commit_epoch, commit_datetime):
        return {
            'start_time': {
                'epoch': commit_epoch,
                'datetime': commit_datetime
            },
            'end_time': {
                'epoch': commit_epoch,
                'datetime': commit_datetime
            },
            'changes': Counter()
        }
