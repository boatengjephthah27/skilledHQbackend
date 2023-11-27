"""
This contains custom decorators that can be used to check that specific 
conditions have been satisfied
"""
from django.core.exceptions import PermissionDenied
from functools import wraps
from core.utils.api_errors import NotAuthorizedError
from core.context import Context



def login_required(function):
  """
  This decorator enforces that a user is logged in before a view can run
  """
  @wraps(function)
  def wrap(handler, request, *args, **kwargs):
    context: Context = request.context
    if context.user_is_logged_in:
      return function(handler, request, *args, **kwargs)
    else:
     return NotAuthorizedError()

  wrap.__doc__ = function.__doc__
  wrap.__name__ = function.__name__
  return wrap

def admins_only(function):
  """
  This decorator enforces that the user is an admin before the view can run
  """
  @wraps(function)
  def wrap(handler, request, *args, **kwargs):
    context: Context = request.context
    if context.user_is_logged_in and context.user_is_admin():
      return function(handler, request, *args, **kwargs)
    else:
      return NotAuthorizedError()
  wrap.__doc__ = function.__doc__
  wrap.__name__ = function.__name__
  return wrap

def partners_only(function):
  """
  This decorator enforces that the user is a community admin before the view can run
  """
  @wraps(function)
  def wrap(handler, request, *args, **kwargs):
    context: Context = request.context
    if context.user_is_logged_in and context.is_partner:
      return function(handler, request, *args, **kwargs)
    else:
      return NotAuthorizedError()
  wrap.__doc__ = function.__doc__
  wrap.__name__ = function.__name__
  return wrap

def super_admins_only(function):
  """
  This decorator enforces that a user is a super admin before the view can run
  """
  @wraps(function)
  def wrap(handler, request, *args, **kwargs):
    context: Context = request.context
    if context.user_is_logged_in and context.is_super_admin:
      return function(handler, request, *args, **kwargs)
    else:
      return NotAuthorizedError()

  wrap.__doc__ = function.__doc__
  wrap.__name__ = function.__name__
  return wrap