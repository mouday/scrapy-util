# -*- coding: utf-8 -*-
import os

class ScrapydUtil(object):

    @classmethod
    def parse_log_file(cls, log_file):
        """
        通过scrapyd调度才会有 LOG_FILE 参数

        LOG_FILE: logs/project/spider/e007e2085fe011ebab89acde48001122.log
        :return:
        """
        if log_file:
            _, project, spider, filename = log_file.split(os.sep)
            job_id, _ = os.path.spiltext(filename)

        else:
            project = ''
            spider = ''
            job_id = ''

        return {
            'project': project,
            'spider': spider,
            'job_id': job_id,
        }
