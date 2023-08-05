# Copyright 2018 Imperva. All rights reserved.

import json
from imperva_sdk.core import *


# Classification Scan - Iris

class ClassificationScan(MxObject):
  '''
  MX Classification Scan Class

  '''

  # Store created Classification Scan objects in _instances to prevent duplicate instances and redundant API calls
  def __new__(ClassType, *args, **kwargs):
    obj_exists = ClassificationScan._exists(connection=kwargs['connection'], Name=kwargs['Name'])
    if obj_exists:
      return obj_exists
    else:
      obj = super(MxObject, ClassType).__new__(ClassType)
      kwargs['connection']._instances.append(obj)
      return obj

  @staticmethod
  def _exists(connection=None, Name=None):
    for cur_obj in connection._instances:
      if type(cur_obj).__name__ == 'ClassificationScan':
        if cur_obj.Name == Name:
          return cur_obj
    return None

  def __init__(self, connection=None, Name=None, ProfileName=None, ApplyTo=[], Scheduling=None):
    super(ClassificationScan, self).__init__(connection=connection, Name=Name)
    validate_string(Name=Name)
    self._ProfileName = ProfileName
    self._ApplyTo = MxList(ApplyTo)
    self._Scheduling = Scheduling

  #
  # Classification Scan Parameters Getters
  #
  @property
  def Name(self):
    ''' The name of the scan (string) '''
    return self._Name

  @property
  def ProfileName(self):
    ''' Name of classification profile (string) '''
    return self._ProfileName

  @property
  def ApplyTo(self):
    '''
    DB Connections that scan is applied to (list of Strings)
    '''
    return self._ApplyTo

  @property
  def Scheduling(self):
    ''' The scan's scheduling '''
    return self._Scheduling

  ##########
  # Setters
  ##########

  @ProfileName.setter
  def ProfileName(self, ProfileName):
    if ProfileName != self._ProfileName:
      self._connection._update_classification_scan(Name=self._Name, Parameter='profileName', Value=ProfileName)
      self._ProfileName = ProfileName

  @ApplyTo.setter
  def ApplyTo(self, ApplyTo):

    tmp1 = []
    for cur_item in ApplyTo:
      tmp1.append(''.join(sorted(str(cur_item))))
    tmp1 = sorted(tmp1)
    tmp2 = []
    for cur_item in self._ApplyTo:
      tmp2 = sorted(tmp2)
      tmp2.append(''.join(sorted(str(cur_item))))
    tmp2 = sorted(tmp2)
    if tmp1 != tmp2:
      self._connection._update_classification_scan(Name=self._Name, Parameter='apply-to', Value=ApplyTo)
      self._ApplyTo = ApplyTo

  @Scheduling.setter
  def Scheduling(self, Scheduling):
    if Scheduling != self._Scheduling:
      self._connection._update_classification_scan(Name=self._Name, Parameter='scheduling', Value=Scheduling)
      self._Scheduling = Scheduling

  ##########################################################
  # static methods for GET ALL, GET, CREATE. DELETE, UPDATE
  ##########################################################

  @staticmethod
  def _get_all_classification_scans(connection):
    try:
      scan_names = connection._mx_api('GET', '/conf/classification/scans')
    except:
      raise MxException("Failed getting Classification Scans")
    scan_objects = []
    for name in scan_names:
      scan_obj = connection.get_classification_scan(Name=name)
      if scan_obj:
        scan_objects.append(scan_obj)
    return scan_objects

  @staticmethod
  def _get_classification_scan(connection, Name=None):
    validate_string(Name=Name)
    obj_exists = ClassificationScan._exists(connection=connection, Name=Name)
    if obj_exists:
      return obj_exists
    try:
      res = connection._mx_api('GET', '/conf/classification/scans/%s' % Name)
    except:
      return None

    if 'profile-name' not in res: res['profile-name'] = None
    if 'apply-to' not in res: res['apply-to'] = []

    ApplyToObjects = []
    for cur_apply in res['apply-to']:
      ApplyToObjects.append(cur_apply)

    return ClassificationScan(connection=connection, Name=Name, ProfileName=res['profile-name'],
                              ApplyTo=ApplyToObjects, Scheduling=res['scheduling'])

  @staticmethod
  def _create_classification_scan(connection, Name=None, ProfileName=None, ApplyTo=None, Scheduling=None,
                                  update=False):
    validate_string(Name=Name)
    scan = connection.get_classification_scan(Name=Name)
    if scan:
      if not update:
        raise MxException("Scan '%s' already exists" % Name)
      else:
        # Update existing scan
        parameters = dict(locals())
        for cur_key in parameters:
          if is_parameter.match(cur_key) and cur_key != 'Name' and parameters[cur_key] != None:
            setattr(scan, cur_key, parameters[cur_key])
      return scan
    else:
      # Create new scan
      body = {
        'profile-name': ProfileName,
      }
      if Scheduling: body['scheduling'] = Scheduling

      if ApplyTo: body['apply-to'] = ApplyTo
      if Scheduling: body['scheduling'] = Scheduling
      connection._mx_api('POST', '/conf/classification/scans/%s' % Name, data=json.dumps(body))
      return ClassificationScan(connection=connection, Name=Name, ProfileName=ProfileName,
                                ApplyTo=ApplyTo, Scheduling=Scheduling)

  @staticmethod
  def _delete_classification_scan(connection, Name=None):
    validate_string(Name=Name)
    scan = connection.get_classification_scan(Name=Name)
    if scan:
      connection._mx_api('DELETE', '/conf/classification/scans/%s' % Name)
      connection._instances.remove(scan)
      del scan
    else:
      raise MxException("Scan does not exist")
    return True

  @staticmethod
  def _update_classification_scan(connection, Name=None, Parameter=None, Value=None):
    body = {Parameter: Value}
    connection._mx_api('PUT', '/conf/classification/scans/%s' % Name, data=json.dumps(body))

    return True




