from god import *

if __name__ == '__main__' :
    import unittest
    
    class TestBasic(unittest.TestCase) :
        def test1(self) :
            script.clear()
            self.assertEquals(script.out(),"#N canvas 100 100 100 100 10;\r\n")
            out = dac(sin(880))
            self.assertEquals(script.out(), """#N canvas 100 100 100 100 10;\r
#X obj 50 40 osc~ 880;\r
#X obj 50 80 dac~;\r
#X connect 0 0 1 0;\r
#X connect 0 0 1 1;\r
""")

        def test2(self) :
            script.clear()
            out = dac(sigmult(sin(440),0.3))
            self.assertEquals(script.out(),
"""#N canvas 100 100 100 100 10;\r
#X obj 50 40 osc~ 440;\r
#X obj 50 80 *~ 0.3;\r
#X obj 50 120 dac~;\r
#X connect 0 0 1 0;\r
#X connect 1 0 2 0;\r
#X connect 1 0 2 1;\r
""")

    unittest.main()
    
 
