#!/usr/bin/env python
# Copyright (c) 2019 Radware LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# @author: Leon Meguira, Radware


from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.AgAccessUserNewCfgTable import *
from typing import Optional


class LocalUserParameters(RadwareParametersStruct):
    def __init__(self):
        self.index = None
        self.user_role = None
        self.user_name = None
        self.state = None
        self.admin_password = None
        self.user_password = None
        self.radius_tacacs_fallback = None
        self.language_display = None


LocalUserParameters.__annotations__ = {
    'index': int,
    'user_role': Optional[EnumAgAccessUserCos],
    'user_name': Optional[str],
    'state': Optional[EnumAgAccessUserState],
    'admin_password': Optional[PasswordArgument],
    'user_password': Optional[PasswordArgument],
    'radius_tacacs_fallback': Optional[EnumAgAccessUserBackDoor],
    'language_display': Optional[EnumAgAccessUserLanguage]
}


bean_map = {
    AgAccessUserNewCfgTable: dict(
        struct=LocalUserParameters,
        direct=True,
        attrs=dict(
            UId='index',
            Cos='user_role',
            Name='user_name',
            BackDoor='radius_tacacs_fallback',
            State='state',
            Language='language_display'
        )
    )
}


class LocalUserConfigurator(AlteonConfigurator):
    def __init__(self, alteon_connection):
        super(LocalUserConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: LocalUserParameters) -> LocalUserParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: LocalUserParameters, dry_run: bool) -> str:
        if parameters.admin_password is not None and parameters.user_password is not None:
            user_access = self._entry_bean_instance(parameters)
            user_access.AdminPswd = parameters.admin_password
            user_access.Pswd = parameters.user_password
            user_access.ConfPswd = parameters.user_password
            self._device_api.update(user_access, dry_run=dry_run)
        self._write_device_beans(parameters, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(AgAccessUserNewCfgTable, parameters)


LocalUserConfigurator.__annotations__ = {
    'parameters_class': LocalUserParameters
}
