# SPDX-License-Identifier: MIT
# Copyright (c) 2020 The Authors.

# Authors: Sherif Abdelwahab <@zasherif>
#          Phu Tran          <@phudtran>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:The above copyright
# notice and this permission notice shall be included in all copies or
# substantial portions of the Software.THE SOFTWARE IS PROVIDED "AS IS",
# WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import kopf
import logging
import luigi
from mizar.common.common import *
from mizar.common.constants import *
from mizar.common.wf_factory import *
from mizar.common.wf_param import *
logger = logging.getLogger()

# @kopf.on.delete(group, version, RESOURCES.vpcs)
# def vpc_opr_on_vpc_delete(body, **kwargs):
#     vpc_operator.on_vpc_delete(body, **kwargs)


@kopf.on.resume(group, version, RESOURCES.vpcs, when=LAMBDAS.vpc_status_init)
@kopf.on.update(group, version, RESOURCES.vpcs, when=LAMBDAS.vpc_status_init)
@kopf.on.create(group, version, RESOURCES.vpcs, when=LAMBDAS.vpc_status_init)
def vpc_opr_on_vpc_init(body, spec, **kwargs):
    param = HandlerParam()
    param.name = kwargs['name']
    param.body = body
    param.spec = spec
    run_workflow(wffactory().VpcCreate(param=param))


@kopf.on.resume(group, version, RESOURCES.vpcs, when=LAMBDAS.vpc_status_provisioned)
@kopf.on.update(group, version, RESOURCES.vpcs, when=LAMBDAS.vpc_status_provisioned)
@kopf.on.create(group, version, RESOURCES.vpcs, when=LAMBDAS.vpc_status_provisioned)
def vpc_opr_on_vpc_provisioned(body, spec, **kwargs):
    param = HandlerParam()
    param.name = kwargs['name']
    param.body = body
    param.spec = spec
    param.diff = kwargs['diff']
    run_workflow(wffactory().VpcProvisioned(param=param))


@kopf.on.delete(group, version, RESOURCES.vpcs)
def vpc_opr_on_vpc_delete(body, spec, **kwargs):
    param = HandlerParam()
    param.name = kwargs['name']
    param.body = body
    param.spec = spec
    run_workflow(wffactory().VpcDelete(param=param))
