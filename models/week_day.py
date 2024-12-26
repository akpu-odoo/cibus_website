# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class WeekDaySelect(models.Model):
    _name = "week.day"
    _description = "Week Days"

    name = fields.Char(string="Name")


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _get_translation_frontend_modules_name(cls):
        mods = super(IrHttp, cls)._get_translation_frontend_modules_name()
        return mods + ['cibus_website']
