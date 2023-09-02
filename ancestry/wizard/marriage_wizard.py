from odoo import fields, models

class MarriageWizard(models.TransientModel):
    _name = "marriage.wizard"
    _description = "Create a spouse link between two family tree members"

    spouse_one = fields.Many2one('ancestry.tree.member', string='Spouse One', required=True)
    spouse_two = fields.Many2one('ancestry.tree.member', string='Spouse Two', required=True)

    
    def confirm_marriage(self):
        # record both members as spouses of each other, checking
        # to make sure the records are not duplicated
        if self.spouse_one.id not in self.spouse_two.spouses.ids:
            self.spouse_two.spouses += self.spouse_one
        if self.spouse_two.id not in self.spouse_one.spouses.ids:
            self.spouse_one.spouses += self.spouse_two

        #TODO: merge children of both spouses, and update their mother and father fields

        # automatically merge the children of both spouses
        # self.spouse_one.children += self.spouse_two.children - self.spouse_one.children
        # self.spouse_two.children += self.spouse_one.children - self.spouse_two.children