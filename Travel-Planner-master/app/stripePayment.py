import stripe

class stripePayment:

    def __init__(self) -> None:
        stripe.api_key = 'sk_test_51HKU4hE0Jc4cZcggjtms3EigjPhnINiWZvXa871eyRTdXQ9vEXPqCV4WoCSOZsXO7DobaQCgqEyap5Ct72uaGLPc00i9QFuHI8'
        
    def generate_card_token(self, card_number, exp_month, exp_year, cvc):
        stripe.api_key = 'sk_test_51HKU4hE0Jc4cZcggjtms3EigjPhnINiWZvXa871eyRTdXQ9vEXPqCV4WoCSOZsXO7DobaQCgqEyap5Ct72uaGLPc00i9QFuHI8'
        

        try:
            token = stripe.Token.create(
                card={
                    'number': card_number,
                    'exp_month': exp_month,
                    'exp_year': exp_year,
                    'cvc': cvc
                }
            )
            print('Card is valid!')
            print('Card token:', token.id)
            return 1
        except stripe.error.CardError as e:
            # Handle card validation error
            print('Card validation error:', e.error.message)
            return 0
        except stripe.error.StripeError as e:
            # Handle other Stripe API errors

            print('Stripe API error:', e.error.message)
            return 0
        return 0

    def create_payment_charge(self, tokenid, amount):
        stripe.api_key = "sk_test_51NKl9OA1uMwOJTRs1WM1nI574bQTxxgrzdAAnhxsmV4UzTBaYVoZMbnIz0iEW7Zucvli2BRLHGrz7ziiq47EfmEr002CVvMZ9B"

        payment = stripe.Charge.create(
            amount= int(amount)*100,                  # convert amount to cents
            currency='usd',
            description='Example charge',
            source=tokenid,
        )
        payment_check = payment['paid']    # return True for successfull payment
        return payment_check
    # token = generate_card_token()
    # create_payment_charge("tok_visa", 100)