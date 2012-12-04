################################################################################
#
# This program is part of the SMART Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.1 2010/07/07 13:37:53 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IHardDiskInfo(IComponentInfo):
    """
    Info adapter for HardDisk components.
    """
    status = schema.Int(title=u"Status", readonly=True, group='Overview')
    title = schema.Text(title=u"Title", readonly=True, group='Details')
