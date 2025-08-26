# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestSaleOrderCancelWizard(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ICPSudo = cls.env['ir.config_parameter'].sudo()
        cls.ccp = cls.env['res.partner'].create({'name': 'CC', 'email': 'c@ex.com'})
        cls.sales_user = cls.env['res.users'].create({'name': 'Sales', 'login': 'sales2', 'email': 'sales2@ex.com'})
        cls.sales_user.partner_id.email = 'sales2_partner@ex.com'
        cls.customer = cls.env['res.partner'].create({'name': 'Cust2', 'email': 'cust2@ex.com'})
        cls.order = cls.env['sale.order'].create({'partner_id': cls.customer.id, 'user_id': cls.sales_user.id})

    def test_cancel_default_cc_from_settings(self):
        self.ICPSudo.set_param('cc_email_automation.enable_custom_partner', '1')
        self.ICPSudo.set_param('cc_email_automation.custom_partner_ids', str(self.ccp.id))
        wiz = self.env['sale.order.cancel'].with_context(default_order_id=self.order.id).create({})
        self.assertEqual(wiz.cc_email_partner_ids.ids, [self.ccp.id])

    def test_cancel_fallback_salesperson(self):
        self.ICPSudo.set_param('cc_email_automation.enable_custom_partner', '0')
        self.ICPSudo.set_param('cc_email_automation.custom_partner_ids', '')
        wiz = self.env['sale.order.cancel'].with_context(default_order_id=self.order.id).create({})
        self.assertEqual(wiz.cc_email_partner_ids.ids, [self.sales_user.partner_id.id])
