import hashlib
import json
import warnings
import requests
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3 import exceptions

requests.packages.urllib3.disable_warnings()

class TestFailure(Exception):
  pass
class PrivateTestFailure(Exception):
  pass

class Test(object):
  passed = 0
  numTests = 0
  failFast = False
  private = False

  @classmethod
  def setFailFast(cls):
    cls.failFast = True

  @classmethod
  def setPrivateMode(cls):
    cls.private = True

  @classmethod
  def assertTrue(cls, result, msg=""):
    cls.numTests += 1
    if result == True:
      cls.passed += 1
      print ("1 test passed.")
    else:
      print ("1 test failed. " + msg)
      if cls.failFast:
        if cls.private:
          raise PrivateTestFailure(msg)
        else:
          raise TestFailure(msg)

  @classmethod
  def assertEquals(cls, var, val, msg=""):
    cls.assertTrue(var == val, msg)

  @classmethod
  def assertEqualsHashed(cls, var, hashed_val, msg=""):
    cls.assertEquals(cls._hash(var), hashed_val, msg)

  @classmethod
  def printStats(cls):
    print ("{0} / {1} test(s) passed.".format(cls.passed, cls.numTests) )

  @classmethod
  def _hash(cls, x):
    return hashlib.sha1(str(x)).hexdigest()

class autograder(object):
    """
    A client to use autograder service from databricks notebook.
    """
    #TODO: autograder-api.cloud.databricks.com  --> 79xml2pftf.execute-api.us-west-2.amazonaws.com
    API_URL = 'https://79xml2pftf.execute-api.us-west-2.amazonaws.com/v1'
    USER_SIGNUP_PATH = '/users/signup'
    USERS_REMOVE_PATH = '/users/remove'
    USERS_SET_ADMIN_PATH ='/users/set_admin'
    USERS_GET_LIST_PATH ='/users/get_list'
    USERS_GET_TOKEN_PATH ='/users/get_token'
    SUBMISSION_GET_SUBMISSION_LIST_PTAH = '/submission/get_submission_list'
    SUBMISSION_GET_SUBMISSION_DETAIL_PATH ='/submission/get_submission_detail'
    SUBMISSION_GET_QUEUE_PATH = '/submission/get_queue'
    SUBMISSION_SUBMIT_PATH = '/submission/submit'
    ERROR_SUCCESS = 'Success.'
    ALL_USERS = '*'

    def _perform_query(self,  path, method = 'POST', data = None):
        """set up connection and perform query"""

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", exceptions.InsecureRequestWarning)
            resp = self.session.request(method, autograder.API_URL + path, data=json.dumps(data),
                                        verify=False)

        try:
            resp.raise_for_status()
        except (requests.exceptions.HTTPError, e):
            print('Error: %s' % resp.text)
            raise e
        return resp.json()

    def __init__(self,username = None, private_token = None):
        self.session = requests.Session()
        self.username = username
        self.private_token = private_token

        pass

    def signup(self,username):
        """
        User sign up to autograder with a valid user name. A new signup for same user can not be done within 30 minutes.
        Args:
            username: a valid e-mail to signup. private token will be sent to the e-mail.
        Returns:
            result string.

        """
        data = {'username':username}
        res= self._perform_query(path= autograder.USER_SIGNUP_PATH, data= data)
        return res['message']

    def login(self,username, private_token):
        """
        set username and private_token for autograder client. This operation is lazily excuted.
        It only checks the authentication during some real operation(e.g. submit, get submission list, etc)
        Args:
            username: username for autograder
            private_token: private token for autograder

        Returns:
            None
        """
        self.username = username
        self.private_token = private_token

    def get_token(self,username):
        """
        Request private token to be sent to a valid e-mail.
        Args:
            username: a valid e-mail to request for a registered user
        Returns:
            result string.
        """
        data = {'username': username}
        res = self._perform_query(path=autograder.USERS_GET_TOKEN_PATH, data=data)
        return res['message']

    def submit(self,lab,notebook_url):
        """
        submit a notebook to autograder for grading.
        Args:
            lab: lab ID. e.g. CS101.x-lab0.
            notebook_url: a valid url for a html format databricks notebook.
                         It can be generated with publishing the notebooks from databricks community edition

        Returns:
            result string.
        """
        data = {
            "username": self.username,
            "private_token": self.private_token,
            "lab": lab,
            "notebook_url": notebook_url
        }
        res = self._perform_query(path=autograder.SUBMISSION_SUBMIT_PATH,data=data)
        return res['message']

    def get_submission_list(self, lab, submission_for_user = None):
        """
        Get submission list for a specified lab. Admin user can see all users' submisison list.
        Args:
            lab: lab ID. e.g. CS101.x-lab0.
            submission_for_user: Only required for admin user to get submission list for some user.

        Returns:
            result string.
            submission list. In each item, username, submission_timestamp, submission_id,
                             grading_status, grade, notebook_url, lab and autograder_results are included.
        """

        if submission_for_user == None:
            # nromal user
            data = {
                "username": self.username,
                "private_token": self.private_token,
                "lab": lab
            }
        else:
            # admin user
            data = {
                "username": self.username,
                "private_token": self.private_token,
                "lab": lab,
                "submission_for_user": submission_for_user,
            }
        res = self._perform_query(path=autograder.SUBMISSION_GET_SUBMISSION_LIST_PTAH,data=data)
        results_string = res['message']
        submission_list = res['submission'] if results_string == autograder.ERROR_SUCCESS else None
        return results_string,submission_list

    def get_queue_status(self):
        """

        Returns:
            results_string.
            queue list. In each item, it includes username, submission_id, grade, notebook_url, lab,
                        submission_timestamp and  grading_status.
        """
        data = {'username': self.username,
                "private_token": self.private_token,
                }

        res = self._perform_query(path=autograder.SUBMISSION_GET_QUEUE_PATH, data=data)
        results_string = res['message']
        queue = res['queue'] if results_string == autograder.ERROR_SUCCESS else None
        return res['message'],queue

    def get_submission_detail(self,submission_id , submission_for_user = None):
        """
        Get submission detail for a submission. Normal user can only check his own submission,
        admin user can check all submissions.
        Args:
            submission_id: submission token id. This can be got from get_submission_list().
            submission_for_user: Only required for admin user to get submission detail for some user.

        Returns:
            results string
            submission detail. In each item, in includes grading_status, grade, notebook_url, notebook_contents,
                               raw_results and autograder_results.
        """
        if submission_for_user == None:
            # nromal user
            data = {
                "username": self.username,
                "private_token": self.private_token,
                "submission_id": submission_id
            }
        else:
            # admin user
            data = {
                "username": self.username,
                "private_token": self.private_token,
                "submission_id": submission_id,
                "submission_for_user": submission_for_user,
            }
        res = self._perform_query(path=autograder.SUBMISSION_GET_SUBMISSION_DETAIL_PATH, data=data)
        results_string = res['message']
        details = res['detail'] if results_string == autograder.ERROR_SUCCESS else None
        return results_string,details

    def set_admin(self,username_to_set_admin,isAdmin = True):
        """
        Set a user as admin/non-admin. This is admin only function.
        Args:
            users_to_set_admin: The username set as admin/non-admin
            isAdmin: True/False for admin and non-admin

        Returns:
            result string.
        """
        data = {'username': self.username,
                "private_token": self.private_token,
                "username_for_admin": username_to_set_admin,
                "admin": "true" if isAdmin == True else "false"
                }
        res = self._perform_query(path=autograder.USERS_SET_ADMIN_PATH, data=data)
        return res['message']

    def remove_user(self,username_to_remove):
        """
        Remove a user. This is admin only function.
        Args:
            username_to_remove: the username to remove.
        Returns:
            result string.
        """
        data = {'username': self.username,
                "private_token": self.private_token,
                "username_to_remove": username_to_remove,
                }

        res = self._perform_query(path=autograder.USERS_REMOVE_PATH, data=data)
        return res['message']

    def get_user_list(self,keyword = '*'):
        """
        Get users list. This is admin only function
        Args:
            keyword: the keyword included for username. If no specified, returns all users

        Returns:
            result string.
            users list. In each item, it includes username, create date and admin/non-admin.
        """
        user_list = []
        if keyword == autograder.ALL_USERS:
            data = {'username': self.username,
                    "private_token": self.private_token,
                    }
        else:
            data = {'username': self.username,
                    "private_token": self.private_token,
                    'keywords': keyword
                    }

        res = self._perform_query(path=autograder.USERS_GET_LIST_PATH, data=data)
        results_string = res['message']
        user_list = res['users'] if results_string == autograder.ERROR_SUCCESS else None
        return results_string,user_list


# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def prepareSubplot(xticks, yticks, figsize=(10.5, 6), hideLabels=False, gridColor='#999999',
                gridWidth=1.0, subplots=(1, 1)):
    """Template for generating the plot layout."""
    plt.close()
    fig, axList = plt.subplots(subplots[0], subplots[1], figsize=figsize, facecolor='white',
                               edgecolor='white')
    if not isinstance(axList, np.ndarray):
        axList = np.array([axList])
        
    for ax in axList.flatten():
        ax.axes.tick_params(labelcolor='#999999', labelsize='10')
        for axis, ticks in [(ax.get_xaxis(), xticks), (ax.get_yaxis(), yticks)]:
            axis.set_ticks_position('none')
            axis.set_ticks(ticks)
            axis.label.set_color('#999999')
            if hideLabels: axis.set_ticklabels([])
        ax.grid(color=gridColor, linewidth=gridWidth, linestyle='-')
        map(lambda position: ax.spines[position].set_visible(False), ['bottom', 'top', 'left', 'right'])
        
    if axList.size == 1:
        axList = axList[0]  # Just return a single axes object for a regular plot
    return fig, axList
    

from pyspark.sql import DataFrame
import inspect
def printDataFrames(verbose=False):
    frames = inspect.getouterframes(inspect.currentframe())
    notebookGlobals = frames[1][0].f_globals
    for k,v in notebookGlobals.items():
        if isinstance(v, DataFrame) and '_' not in k:
            print ("{0}: {1}".format(k, v.columns) if verbose else "{0}".format(k) )

if __name__ == '__main__':
    printDataFrames()


def printLocalFunctions(verbose=False):
    frames = inspect.getouterframes(inspect.currentframe())
    notebookGlobals = frames[1][0].f_globals
    import types
    ourFunctions = [(k, v.__doc__) for k,v in notebookGlobals.items() if isinstance(v, types.FunctionType) and v.__module__ == '__main__']
    
    for k,v in ourFunctions:
        print ("** {0} **".format(k))
        if verbose:
            print (v)
        
if __name__ == '__main__':
    printLocalFunctions()
        
        
from collections import Iterable
asSelf = lambda v: map(lambda r: r[0] if isinstance(r, Iterable) and len(r) == 1 else r, v)


