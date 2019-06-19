"""
My own creation for the Test object.
"""
class MyTest:
    def describe(self, s):
        print('==================')
        print(s)

    def assert_equals(self, output, answer):
        print("++++", output == answer)
        if output != answer:
            print("Incorrect output:")
            print([output])
            print("Desired output:")
            print([answer])

    def it(self,s):
        print('')
        print(s)

    def expect(self, passed, output):
        print("++++", passed)
        if not passed:
            print('Actual output:')
            print([output])


