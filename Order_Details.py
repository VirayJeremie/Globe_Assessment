class Order_Details:
        def __init__(self):
            self.Ordered_item = 'Dotted Shirt'
            self.Ordered_Size = 'M'
            self.Ordered_Color = 'White'
            self.Clothing_Detail = 'Color: ' + self.Ordered_Size + ',' + 'Size: ' + self.Ordered_Size  
            self.Confirmed_Order = 'Your order is confirmed!'
            self.Ordered_Quantity = 1
            self.Ordered_Price = self.Ordered_Quantity * 54.99