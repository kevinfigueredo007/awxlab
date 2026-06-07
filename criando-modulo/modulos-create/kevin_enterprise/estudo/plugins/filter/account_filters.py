class FilterModule:

    def filters(self):

        return {
            "mask_account": self.mask_account
        }

    def mask_account(self, value):
        return value[:4] + "********"
