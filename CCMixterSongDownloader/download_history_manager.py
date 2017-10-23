import os
import logging
import json


class History:
    log_file = '._history.json'

    @staticmethod
    def history_log(wdir=os.getcwd(), log_file='log_file.txt',
                    mode='read', write_data=None):
        """This should generally be called after another program has finished
        to record it's progress or history.
        Read python dictionary from or write python dictionary to a file

        :param wdir: directory for text file to be saved to
        :param log_file: name of text file (include .txt extension)
        :param mode: 'read', 'write', or 'append' are valid
        :param write_data: data that'll get written in the log_file
        :type write_data: dictionary (or list or set)

        :return: returns data read from or written to file (depending on mode)
        :rtype: dictionary
        """
        mode_dict = {
            'read': 'r',
            'write': 'w',
            'append': 'a'
        }
        if mode in mode_dict:
            with open(os.path.join(wdir, log_file), mode_dict[mode]) as f:
                if mode == 'read':
                    return json.loads(f.read())
                else:
                    f.write(json.dumps(write_data))
                    return write_data
        else:
            logging.debug('history_log func: invalid mode (param #3)')
            return {}

    @staticmethod
    def get_previous_download_amount(tags, sort, dir, verbose=False):
        """Open & update log_file to get last_id of subreddit of sort_type
        Creates log_file if no existing log file was found

        :param tags: name of subreddit
        :param sort: sort type of subreddit
        :param dir: directory log_file will be saved to
        :param log_file: name of log file
        :param verbose: prints extra messages

        :return: log_data (contains last ids), last_id
        :rtype: tuple

        Note: this has been modified to work with CCMixterSongDownloader
        """
        no_history = False
        try:
            # first: we try to open the log_file
            log_data = History.history_log(dir, History.log_file, 'read')

            # second: we check if the data loaded is a dictionary
            if not isinstance(log_data, dict):
                raise ValueError(
                    log_data,
                    'data from %s is not a dictionary, overwriting %s'
                    % (History.log_file, History.log_file))

            # third: try loading last id for subreddit & sort_type
            if tags in log_data:
                if sort in log_data[tags]:
                    last_id = log_data[tags][sort]['downloads']
                else:  # sort not in log_data but tags is
                    no_history = True
                    log_data[tags][sort] = {'downloads': 0}
            else:  # tags not listed as key in log_data
                no_history = True
                log_data[tags] = {sort: {'downloads': 0}}

        # py3 or py2 exception for dne file
        except (FileNotFoundError, IOError, FileExistsError):
            last_id = ''
            log_data = {
                tags: {
                    sort: {
                        'downloads': 0
                    }
                }
            }
            History.history_log(dir, History.log_file, 'write', log_data)
            if verbose:
                print('%s not found in %s, created new %s'
                      % (History.log_file, dir, History.log_file))

        except ValueError as e:
            if verbose:
                print('log_data:\n{}'.format(e.args))

        except Exception as e:
            print(e)

        if no_history:
            last_id = 0
            log_data = History.history_log(dir, History.log_file, 'write',
                                           log_data)

        return log_data, last_id
