from __future__ import with_statement
from contextpy import layer, proceed, activelayer, activelayers, inactivelayer, after, around, before, base, globalActivateLayer, globalDeactivateLayer
import contextpy
import time
import gc

INITSIZE = 200000 # was 10000
MAXSIZE = 1000000000
TARGETTIME = 5.0

l01 = layer("layer 1")
l02 = layer("layer 2")
l03 = layer("layer 3")
l04 = layer("layer 4")
l05 = layer("layer 5")
l06 = layer("layer 6")
l07 = layer("layer 7")
l08 = layer("layer 8")
l09 = layer("layer 9")
l10 = layer("layer 10")
# l11 = layer("layer 11")
# l12 = layer("layer 12")
# l13 = layer("layer 13")
# l14 = layer("layer 14")

class ContextPyMethodBench2(object):

    counter_00 = 0
    counter_01 = 0
    counter_02 = 0
    counter_03 = 0
    counter_04 = 0
    counter_05 = 0
    counter_06 = 0
    counter_07 = 0
    counter_08 = 0
    counter_09 = 0
    counter_10 = 0
    # counter_11 = 0
    # counter_12 = 0
    # counter_13 = 0
    # counter_14 = 0
    ## counter_15 = 0

    def resetCounter(self):
        self.counter_00 = 0
        self.counter_01 = 0
        self.counter_02 = 0
        self.counter_03 = 0
        self.counter_04 = 0
        self.counter_05 = 0
        self.counter_06 = 0
        self.counter_07 = 0
        self.counter_08 = 0
        self.counter_09 = 0
        self.counter_10 = 0
        # self.counter_11 = 0
        # self.counter_12 = 0
        # self.counter_13 = 0
        # self.counter_14 = 0
        ## self.counter_15 = 0

    def noLayer_01(self):
        self.counter_01 += 1

    def noLayer_02(self):
        self.counter_01 += 1
        self.counter_02 += 1

    def noLayer_03(self):
        self.counter_01 += 1
        self.counter_02 += 1
        self.counter_03 += 1

    def noLayer_04(self):
        self.counter_01 += 1
        self.counter_02 += 1
        self.counter_03 += 1
        self.counter_04 += 1

    def noLayer_05(self):
        self.counter_01 += 1
        self.counter_02 += 1
        self.counter_03 += 1
        self.counter_04 += 1
        self.counter_05 += 1

    def noLayer_06(self):
        self.counter_01 += 1
        self.counter_02 += 1
        self.counter_03 += 1
        self.counter_04 += 1
        self.counter_05 += 1
        self.counter_06 += 1

    def noLayer_07(self):
        self.counter_01 += 1
        self.counter_02 += 1
        self.counter_03 += 1
        self.counter_04 += 1
        self.counter_05 += 1
        self.counter_06 += 1
        self.counter_07 += 1

    def noLayer_08(self):
        self.counter_01 += 1
        self.counter_02 += 1
        self.counter_03 += 1
        self.counter_04 += 1
        self.counter_05 += 1
        self.counter_06 += 1
        self.counter_07 += 1
        self.counter_08 += 1

    def noLayer_09(self):
        self.counter_01 += 1
        self.counter_02 += 1
        self.counter_03 += 1
        self.counter_04 += 1
        self.counter_05 += 1
        self.counter_06 += 1
        self.counter_07 += 1
        self.counter_08 += 1
        self.counter_09 += 1

    def noLayer_10(self):
        self.counter_01 += 1
        self.counter_02 += 1
        self.counter_03 += 1
        self.counter_04 += 1
        self.counter_05 += 1
        self.counter_06 += 1
        self.counter_07 += 1
        self.counter_08 += 1
        self.counter_09 += 1
        self.counter_10 += 1

    # def noLayer_11(self):
    #     self.counter_01 += 1
    #     self.counter_02 += 1
    #     self.counter_03 += 1
    #     self.counter_04 += 1
    #     self.counter_05 += 1
    #     self.counter_06 += 1
    #     self.counter_07 += 1
    #     self.counter_08 += 1
    #     self.counter_09 += 1
    #     self.counter_10 += 1
    #     self.counter_11 += 1
    #
    # def noLayer_12(self):
    #     self.counter_01 += 1
    #     self.counter_02 += 1
    #     self.counter_03 += 1
    #     self.counter_04 += 1
    #     self.counter_05 += 1
    #     self.counter_06 += 1
    #     self.counter_07 += 1
    #     self.counter_08 += 1
    #     self.counter_09 += 1
    #     self.counter_10 += 1
    #     self.counter_11 += 1
    #     self.counter_12 += 1
    #
    # def noLayer_13(self):
    #     self.counter_01 += 1
    #     self.counter_02 += 1
    #     self.counter_03 += 1
    #     self.counter_04 += 1
    #     self.counter_05 += 1
    #     self.counter_06 += 1
    #     self.counter_07 += 1
    #     self.counter_08 += 1
    #     self.counter_09 += 1
    #     self.counter_10 += 1
    #     self.counter_11 += 1
    #     self.counter_12 += 1
    #     self.counter_13 += 1
    #
    # def noLayer_14(self):
    #     self.counter_01 += 1
    #     self.counter_02 += 1
    #     self.counter_03 += 1
    #     self.counter_04 += 1
    #     self.counter_05 += 1
    #     self.counter_06 += 1
    #     self.counter_07 += 1
    #     self.counter_08 += 1
    #     self.counter_09 += 1
    #     self.counter_10 += 1
    #     self.counter_11 += 1
    #     self.counter_12 += 1
    #     self.counter_13 += 1
    #     self.counter_14 += 1
    #
    ## def noLayer_15(self):
    ##     self.counter_01 += 1
    ##     self.counter_02 += 1
    ##     self.counter_03 += 1
    ##     self.counter_04 += 1
    ##     self.counter_05 += 1
    ##     self.counter_06 += 1
    ##     self.counter_07 += 1
    ##     self.counter_08 += 1
    ##     self.counter_09 += 1
    ##     self.counter_10 += 1
    ##     self.counter_11 += 1
    ##     self.counter_12 += 1
    ##     self.counter_13 += 1
    ##     self.counter_14 += 1
    ##     self.counter_15 += 1

    @base
    def withLayer(self):
        pass # cf. contextl-benchmark.lisp
        # self.counter_00 += 1

    @around(l01)
    def withLayer(self):
        proceed()
        self.counter_01 += 1

    @around(l02)
    def withLayer(self):
        proceed()
        self.counter_02 += 1

    @around(l03)
    def withLayer(self):
        proceed()
        self.counter_03 += 1

    @around(l04)
    def withLayer(self):
        proceed()
        self.counter_04 += 1

    @around(l05)
    def withLayer(self):
        proceed()
        self.counter_05 += 1

    @around(l06)
    def withLayer(self):
        proceed()
        self.counter_06 += 1

    @around(l07)
    def withLayer(self):
        proceed()
        self.counter_07 += 1

    @around(l08)
    def withLayer(self):
        proceed()
        self.counter_08 += 1

    @around(l09)
    def withLayer(self):
        proceed()
        self.counter_09 += 1

    @around(l10)
    def withLayer(self):
        proceed()
        self.counter_10 += 1

    # @around(l11)
    # def withLayer(self):
    #     proceed()
    #     self.counter_11 += 1
    #
    # @around(l12)
    # def withLayer(self):
    #     proceed()
    #     self.counter_12 += 1
    #
    # @around(l13)
    # def withLayer(self):
    #     proceed()
    #     self.counter_13 += 1
    #
    # @around(l14)
    # def withLayer(self):
    #     proceed()
    #     self.counter_14 += 1

    # def withoutLayers(self, l01=False,  l02=False,  l03=False,  l04=False,  l05=False,  l06=False,  l07=False,  l08=False,  l09=False,  l10=False,  l11=False,  l12=False,  l13=False,  l14=False):
    def withoutLayers(self, l01=False,  l02=False,  l03=False,  l04=False,  l05=False,  l06=False,  l07=False,  l08=False,  l09=False,  l10=False):
        if l01:
            self.counter_01 += 1
        if l02:
            self.counter_02 += 1
        if l03:
            self.counter_03 += 1
        if l04:
            self.counter_04 += 1
        if l05:
            self.counter_05 += 1
        if l06:
            self.counter_06 += 1
        if l07:
            self.counter_07 += 1
        if l08:
            self.counter_08 += 1
        if l09:
            self.counter_09 += 1
        if l10:
            self.counter_10 += 1
        # if l11:
        #     self.counter_11 += 1
        # if l12:
        #     self.counter_12 += 1
        # if l13:
        #     self.counter_13 += 1
        # if l14:
        #     self.counter_14 += 1
        ## if l15:
        ##     self.counter_15 += 1

    def runMethod(self, label, method):
        timer = Timer()
        self.resetCounter()
        consumedTime = 0.0
        rangeList = range(16) # Speed Up
        size = INITSIZE
        while consumedTime < TARGETTIME and size < MAXSIZE:
            timer.resetTimer()
            timer.startTimer()
            for i in xrange(size):
                for j in rangeList:
                    method()
            timer.stopTimer()
            consumedTime = timer.readTimer()
            timer.addOpsToTimer(16*size)
            size *= 2
        print "%s\t%s" % (label, timer.printPerfTimer())
        #print self.counter_01, self.counter_02, self.counter_03, self.counter_04


    def runMethodWithLayers(self, label, *layers):
        timer = Timer()
        self.resetCounter()
        consumedTime = 0.0
        rangeList = range(16) # Speed Up
        size = INITSIZE
        while consumedTime < TARGETTIME and size < MAXSIZE:
            timer.resetTimer()

            with activelayers(*layers):
                timer.startTimer()
                for i in xrange(size):
                    for j in rangeList:
                        self.withLayer()
                timer.stopTimer()

            consumedTime = timer.readTimer()
            timer.addOpsToTimer(16*size)
            size *= 2
        print "%s\t%s" % (label, timer.printPerfTimer())
        #print self.counter_01, self.counter_02, self.counter_03, self.counter_04

    def runMethodWithoutLayers(self, label, **layers):
        timer = Timer()
        self.resetCounter()
        consumedTime = 0.0
        rangeList = range(16) # Speed Up
        size = INITSIZE
        while consumedTime < TARGETTIME and size < MAXSIZE:
            timer.resetTimer()

            timer.startTimer()
            for i in xrange(size):
                for j in rangeList:
                    self.withoutLayers(**layers)
            timer.stopTimer()

            consumedTime = timer.readTimer()
            timer.addOpsToTimer(16*size)
            size *= 2
        print "%s\t%s" % (label, timer.printPerfTimer())
        #print self.counter_01, self.counter_02, self.counter_03, self.counter_04

    def run(self, num_layers, arg):
        gc.disable()

        if arg == 'standard':
            if False: pass
            elif num_layers == 0:
                self.runMethodWithoutLayers("ContextPy:Method:Standard:0")
            elif num_layers == 1:
                self.runMethodWithoutLayers("ContextPy:Method:Standard:1", l01=True)
            elif num_layers == 2:
                self.runMethodWithoutLayers("ContextPy:Method:Standard:2", l01=True,l02=True)
            elif num_layers == 3:
                self.runMethodWithoutLayers("ContextPy:Method:Standard:3", l01=True,l02=True,l03=True)
            elif num_layers == 4:
                self.runMethodWithoutLayers("ContextPy:Method:Standard:4", l01=True,l02=True,l03=True,l04=True)
            elif num_layers == 5:
                self.runMethodWithoutLayers("ContextPy:Method:Standard:5", l01=True,l02=True,l03=True,l04=True,l05=True)
            elif num_layers == 6:
                self.runMethodWithoutLayers("ContextPy:Method:Standard:6", l01=True,l02=True,l03=True,l04=True,l05=True,l06=True)
            elif num_layers == 7:
                self.runMethodWithoutLayers("ContextPy:Method:Standard:7", l01=True,l02=True,l03=True,l04=True,l05=True,l06=True,l07=True)
            elif num_layers == 8:
                self.runMethodWithoutLayers("ContextPy:Method:Standard:8", l01=True,l02=True,l03=True,l04=True,l05=True,l06=True,l07=True,l08=True)
            elif num_layers == 9:
                self.runMethodWithoutLayers("ContextPy:Method:Standard:9", l01=True,l02=True,l03=True,l04=True,l05=True,l06=True,l07=True,l08=True,l09=True)
            elif num_layers == 10:
                self.runMethodWithoutLayers("ContextPy:Method:Standard:10", l01=True,l02=True,l03=True,l04=True,l05=True,l06=True,l07=True,l08=True,l09=True,l10=True)
            else:
                print "too many layers %d for %s" % (num_layers, arg)
                exit(3)

        elif arg == 'nolayer':
            if False: pass
            elif num_layers == 0:
                pass
                # self.runMethodWithoutLayers("ContextPy:Method:NoLayer:0")
            elif num_layers == 1:
                self.runMethod("ContextPy:Method:NoLayer:1", self.noLayer_01)
            elif num_layers == 2:
                self.runMethod("ContextPy:Method:NoLayer:2", self.noLayer_02)
            elif num_layers == 3:
                self.runMethod("ContextPy:Method:NoLayer:3", self.noLayer_03)
            elif num_layers == 4:
                self.runMethod("ContextPy:Method:NoLayer:4", self.noLayer_04)
            elif num_layers == 5:
                self.runMethod("ContextPy:Method:NoLayer:5", self.noLayer_05)
            elif num_layers == 6:
                self.runMethod("ContextPy:Method:NoLayer:6", self.noLayer_06)
            elif num_layers == 7:
                self.runMethod("ContextPy:Method:NoLayer:7", self.noLayer_07)
            elif num_layers == 8:
                self.runMethod("ContextPy:Method:NoLayer:8", self.noLayer_08)
            elif num_layers == 9:
                self.runMethod("ContextPy:Method:NoLayer:9", self.noLayer_09)
            elif num_layers == 10:
                self.runMethod("ContextPy:Method:NoLayer:10", self.noLayer_10)
            else:
                print "too many layers %d for %s" % (num_layers, arg)
                exit(3)

        elif arg == 'layer':
            if False: pass
            elif num_layers == 0:
                self.runMethodWithLayers("ContextPy:Method:WithLayer:0")
            elif num_layers == 1:
                self.runMethodWithLayers("ContextPy:Method:WithLayer:1", l01)
            elif num_layers == 2:
                self.runMethodWithLayers("ContextPy:Method:WithLayer:2", l01,l02)
            elif num_layers == 3:
                self.runMethodWithLayers("ContextPy:Method:WithLayer:3", l01,l02,l03)
            elif num_layers == 4:
                self.runMethodWithLayers("ContextPy:Method:WithLayer:4", l01,l02,l03,l04)
            elif num_layers == 5:
                self.runMethodWithLayers("ContextPy:Method:WithLayer:5", l01,l02,l03,l04,l05)
            elif num_layers == 6:
                self.runMethodWithLayers("ContextPy:Method:WithLayer:6", l01,l02,l03,l04,l05,l06)
            elif num_layers == 7:
                self.runMethodWithLayers("ContextPy:Method:WithLayer:7", l01,l02,l03,l04,l05,l06,l07)
            elif num_layers == 8:
                self.runMethodWithLayers("ContextPy:Method:WithLayer:8", l01,l02,l03,l04,l05,l06,l07,l08)
            elif num_layers == 9:
                self.runMethodWithLayers("ContextPy:Method:WithLayer:9", l01,l02,l03,l04,l05,l06,l07,l08,l09)
            elif num_layers == 10:
                self.runMethodWithLayers("ContextPy:Method:WithLayer:10", l01,l02,l03,l04,l05,l06,l07,l08,l09,l10)
            else:
                print "too many layers %d for %s" % (num_layers, arg)
                exit(3)

        #self.runMethod("ContextPy:Method:Layer", self.withLayer)
        # self.runMethodWithLayers("ContextPy:Method:Layer:1", l01)
        # self.runMethodWithLayers("ContextPy:Method:Layer:2", l01,l02)
        # self.runMethodWithLayers("ContextPy:Method:Layer:3", l01,l02,l03)
        # self.runMethodWithLayers("ContextPy:Method:Layer:4", l01,l02,l03,l04)
        # self.runMethodWithLayers("ContextPy:Method:Layer:5", l01,l02,l03,l04,l05)
        # self.runMethodWithLayers("ContextPy:Method:Layer:6", l01,l02,l03,l04,l05,l06)
        # self.runMethodWithLayers("ContextPy:Method:Layer:7", l01,l02,l03,l04,l05,l06,l07)
        # self.runMethodWithLayers("ContextPy:Method:Layer:8", l01,l02,l03,l04,l05,l06,l07,l08)
        # self.runMethodWithLayers("ContextPy:Method:Layer:9", l01,l02,l03,l04,l05,l06,l07,l08,l09)
        # self.runMethodWithLayers("ContextPy:Method:Layer:10", l01,l02,l03,l04,l05,l06,l07,l08,l09,l10)
        # self.runMethodWithLayers("ContextPy:Method:Layer:11", l01,l02,l03,l04,l05,l06,l07,l08,l09,l10,l11)
        # self.runMethodWithLayers("ContextPy:Method:Layer:12", l01,l02,l03,l04,l05,l06,l07,l08,l09,l10,l11,l12)
        # self.runMethodWithLayers("ContextPy:Method:Layer:13", l01,l02,l03,l04,l05,l06,l07,l08,l09,l10,l11,l12,l13)
        # self.runMethodWithLayers("ContextPy:Method:Layer:14", l01,l02,l03,l04,l05,l06,l07,l08,l09,l10,l11,l12,l13,l14)

        else:
            print "can't handle this arg: %s" % arg
            exit(2)

        # print "End Method Benchmark"
        gc.enable()


class ContextPyLayerActivationBench(object):

    counter_01 = 0
    counter_02 = 0
    counter_03 = 0
    counter_04 = 0
    counter_05 = 0
    # counter_06 = 0
    # counter_07 = 0
    # counter_08 = 0
    # counter_09 = 0
    # counter_10 = 0
    # counter_11 = 0
    # counter_12 = 0
    # counter_13 = 0
    # counter_14 = 0
    # counter_15 = 0

    def resetCounter(self):
        self.counter_01 = 0
        self.counter_02 = 0
        self.counter_03 = 0
        self.counter_04 = 0
        self.counter_05 = 0
        # self.counter_06 = 0
        # self.counter_07 = 0
        # self.counter_08 = 0
        # self.counter_09 = 0
        # self.counter_10 = 0
        # self.counter_11 = 0
        # self.counter_12 = 0
        # self.counter_13 = 0
        # self.counter_14 = 0
        # self.counter_15 = 0

    def u1(self):
        self.counter_01 += 1

    def u2(self):
        self.counter_02 += 1

    def u3(self):
        self.counter_03 += 1

    def u4(self):
        self.counter_04 += 1

    def u5(self):
        self.counter_05 += 1


    def m1(self):
        self.counter_01 += 1

    def m2(self):
        self.counter_02 += 1

    def m3(self):
        self.counter_03 += 1

    def m4(self):
        self.counter_04 += 1

    def m5(self):
        self.counter_05 += 1

    @around(l01)
    def m1(self):
        self.counter_01 += 1

    @around(l01)
    def m2(self):
        self.counter_02 += 1

    @around(l01)
    def m3(self):
        self.counter_03 += 1

    @around(l01)
    def m4(self):
        self.counter_04 += 1

    @around(l01)
    def m5(self):
        self.counter_05 += 1

    @around(l02)
    def m1(self):
        self.counter_01 += 1

    @around(l02)
    def m2(self):
        self.counter_02 += 1

    @around(l02)
    def m3(self):
        self.counter_03 += 1

    @around(l02)
    def m4(self):
        self.counter_04 += 1

    @around(l02)
    def m5(self):
        self.counter_05 += 1

    @around(l03)
    def m1(self):
        self.counter_01 += 1

    @around(l03)
    def m2(self):
        self.counter_02 += 1

    @around(l03)
    def m3(self):
        self.counter_03 += 1

    @around(l03)
    def m4(self):
        self.counter_04 += 1

    @around(l03)
    def m5(self):
        self.counter_05 += 1

    @around(l04)
    def m1(self):
        self.counter_01 += 1

    @around(l04)
    def m2(self):
        self.counter_02 += 1

    @around(l04)
    def m3(self):
        self.counter_03 += 1

    @around(l04)
    def m4(self):
        self.counter_04 += 1

    @around(l04)
    def m5(self):
        self.counter_05 += 1

    @around(l05)
    def m1(self):
        self.counter_01 += 1

    @around(l05)
    def m2(self):
        self.counter_02 += 1

    @around(l05)
    def m3(self):
        self.counter_03 += 1

    @around(l05)
    def m4(self):
        self.counter_04 += 1

    @around(l05)
    def m5(self):
        self.counter_05 += 1


    def runReferenceNoCOP(self, label):
        timer = Timer()
        self.resetCounter()
        consumedTime = 0.0
        rangeList = range(16) # Speed Up
        size = INITSIZE
        while consumedTime < TARGETTIME and size < MAXSIZE:
            timer.resetTimer()
            timer.startTimer()
            for i in xrange(size):
                for j in rangeList:
                    self.u1()
                    self.u2()
                    self.u3()
                    self.u4()
                    self.u5()
            timer.stopTimer()
            consumedTime = timer.readTimer()
            timer.addOpsToTimer(16*size)
            size *= 2
        print label, size, timer.printPerfTimer()

    def runReference(self, label):
        timer = Timer()
        self.resetCounter()
        consumedTime = 0.0
        rangeList = range(16) # Speed Up
        size = INITSIZE
        while consumedTime < TARGETTIME and size < MAXSIZE:
            timer.resetTimer()
            timer.startTimer()
            for i in xrange(size):
                for j in rangeList:
                    self.m1()
                    self.m2()
                    self.m3()
                    self.m4()
                    self.m5()
            timer.stopTimer()
            consumedTime = timer.readTimer()
            timer.addOpsToTimer(16*size)
            size *= 2
        print "%s\t%s" % (label, timer.printPerfTimer())

    def runMethodWithLayers(self, label, *layers):
        timer = Timer()
        self.resetCounter()
        consumedTime = 0.0
        rangeList = range(16) # Speed Up
        size = INITSIZE
        while consumedTime < TARGETTIME and size < MAXSIZE:
            timer.resetTimer()
            timer.startTimer()
            for i in xrange(size):
                for j in rangeList:
                    with activelayers(*layers):
                        self.m1()
                        self.m2()
                        self.m3()
                        self.m4()
                        self.m5()
            timer.stopTimer()
            consumedTime = timer.readTimer()
            timer.addOpsToTimer(16*size)
            size *= 2
        print "%s\t%s" % (label, timer.printPerfTimer())

    def runMethodWithNestedLayers1(self, label):
        timer = Timer()
        self.resetCounter()
        consumedTime = 0.0
        rangeList = range(16) # Speed Up
        size = INITSIZE
        while consumedTime < TARGETTIME and size < MAXSIZE:
            timer.resetTimer()
            timer.startTimer()
            for i in xrange(size):
                for j in rangeList:
                    with activelayer(l01):
                        self.m1()
                        self.m2()
                        self.m3()
                        self.m4()
                        self.m5()
            timer.stopTimer()
            consumedTime = timer.readTimer()
            timer.addOpsToTimer(16*size)
            size *= 2
        print "%s\t%s" % (label, timer.printPerfTimer())

    def runMethodWithNestedLayers2(self, label):
        timer = Timer()
        self.resetCounter()
        consumedTime = 0.0
        rangeList = range(16) # Speed Up
        size = INITSIZE
        while consumedTime < TARGETTIME and size < MAXSIZE:
            timer.resetTimer()
            timer.startTimer()
            for i in xrange(size):
                for j in rangeList:
                    with activelayer(l01):
                        self.m1()
                        with activelayer(l02):
                            self.m2()
                            self.m3()
                            self.m4()
                            self.m5()
            timer.stopTimer()
            consumedTime = timer.readTimer()
            timer.addOpsToTimer(16*size)
            size *= 2
        print "%s\t%s" % (label, timer.printPerfTimer())

    def runMethodWithNestedLayers3(self, label):
        timer = Timer()
        self.resetCounter()
        consumedTime = 0.0
        rangeList = range(16) # Speed Up
        size = INITSIZE
        while consumedTime < TARGETTIME and size < MAXSIZE:
            timer.resetTimer()
            timer.startTimer()
            for i in xrange(size):
                for j in rangeList:
                    with activelayer(l01):
                        self.m1()
                        with activelayer(l02):
                            self.m2()
                            with activelayer(l03):
                                self.m3()
                                self.m4()
                                self.m5()
            timer.stopTimer()
            consumedTime = timer.readTimer()
            timer.addOpsToTimer(16*size)
            size *= 2
        print "%s\t%s" % (label, timer.printPerfTimer())

    def runMethodWithNestedLayers4(self, label):
        timer = Timer()
        self.resetCounter()
        consumedTime = 0.0
        rangeList = range(16) # Speed Up
        size = INITSIZE
        while consumedTime < TARGETTIME and size < MAXSIZE:
            timer.resetTimer()
            timer.startTimer()
            for i in xrange(size):
                for j in rangeList:
                    with activelayer(l01):
                        self.m1()
                        with activelayer(l02):
                            self.m2()
                            with activelayer(l03):
                                self.m3()
                                with activelayer(l04):
                                    self.m4()
                                    self.m5()
            timer.stopTimer()
            consumedTime = timer.readTimer()
            timer.addOpsToTimer(16*size)
            size *= 2
        print "%s\t%s" % (label, timer.printPerfTimer())

    def runMethodWithNestedLayers5(self, label):
        timer = Timer()
        self.resetCounter()
        consumedTime = 0.0
        rangeList = range(16) # Speed Up
        size = INITSIZE
        while consumedTime < TARGETTIME and size < MAXSIZE:
            timer.resetTimer()
            timer.startTimer()
            for i in xrange(size):
                for j in rangeList:
                    with activelayer(l01):
                        self.m1()
                        with activelayer(l02):
                            self.m2()
                            with activelayer(l03):
                                self.m3()
                                with activelayer(l04):
                                    self.m4()
                                    with activelayer(l05):
                                        self.m5()
            timer.stopTimer()
            consumedTime = timer.readTimer()
            timer.addOpsToTimer(16*size)
            size *= 2
        print "%s\t%s" % (label, timer.printPerfTimer())

    def run(self,num_layers,arg):
        gc.disable()
        # print "Start WITH Benchmark"
        # self.runReferenceNoCOP("ContextPy:Normal")
        # self.runReference("ContextPy:With:NoLayer")
        #
        # self.runMethodWithLayers("ContextPy:With:Layer:1", l01)
        # self.runMethodWithLayers("ContextPy:With:Layer:2", l01,l02)
        # self.runMethodWithLayers("ContextPy:With:Layer:3", l01,l02,l03)
        # self.runMethodWithLayers("ContextPy:With:Layer:4", l01,l02,l03,l04)
        # self.runMethodWithLayers("ContextPy:With:Layer:5", l01,l02,l03,l04,l05)
        # self.runMethodWithNestedLayers1("ContextPy:WithNested:Layer:1")
        # self.runMethodWithNestedLayers2("ContextPy:WithNested:Layer:2")
        # self.runMethodWithNestedLayers3("ContextPy:WithNested:Layer:3")
        # self.runMethodWithNestedLayers4("ContextPy:WithNested:Layer:4")
        # self.runMethodWithNestedLayers5("ContextPy:WithNested:Layer:5")

        if arg == 'flat':
            if False: pass
            elif num_layers == 0:
                self.runReference("ContextPy:ActivateLayerFlat:0")
            elif num_layers == 1:
                self.runMethodWithLayers("ContextPy:ActivateLayerFlat:1", l01)
            elif num_layers == 2:
                self.runMethodWithLayers("ContextPy:ActivateLayerFlat:2", l01,l02)
            elif num_layers == 3:
                self.runMethodWithLayers("ContextPy:ActivateLayerFlat:3", l01,l02,l03)
            elif num_layers == 4:
                self.runMethodWithLayers("ContextPy:ActivateLayerFlat:4", l01,l02,l03,l04)
            elif num_layers == 5:
                self.runMethodWithLayers("ContextPy:ActivateLayerFlat:5", l01,l02,l03,l04,l05)
            else:
                print "too many layers %d for %s" % (num_layers, arg)
                exit(3)

        elif arg == 'nested':
            if False: pass
            elif num_layers == 0:
                self.runReference("ContextPy:ActivateLayer:0")
            elif num_layers == 1:
                self.runMethodWithNestedLayers1("ContextPy:ActivateLayer:1")
            elif num_layers == 2:
                self.runMethodWithNestedLayers2("ContextPy:ActivateLayer:2")
            elif num_layers == 3:
                self.runMethodWithNestedLayers3("ContextPy:ActivateLayer:3")
            elif num_layers == 4:
                self.runMethodWithNestedLayers4("ContextPy:ActivateLayer:4")
            elif num_layers == 5:
                self.runMethodWithNestedLayers5("ContextPy:ActivateLayer:5")
            else:
                print "too many layers %d for %s" % (num_layers, arg)
                exit(3)

        else:
            print "can't handle this arg: %s" % arg
            exit(2)

        # print "End WITH Benchmark"
        gc.enable()


class Timer(object):
    def __init__(self):
        self.value = 0.0
        self.numberOfOpps = 0

    def resetTimer(self):
        self.value = 0.0

    def startTimer(self):
        self.startTime = time.time()

    def stopTimer(self):
        self.stopTime = time.time()
        self.value = self.stopTime - self.startTime

    def readTimer(self):
        return self.value

    def addOpsToTimer(self, numberOfOpps):
        self.numberOfOpps = numberOfOpps

    def printPerfTimer(self):
        # return "Number of Opps:", self.numberOfOpps / (self.value * 1000.0)
        return "%d\t%d\t%d" % (self.numberOfOpps, self.value * 1000.0, self.numberOfOpps / (self.value * 1000.0))


if __name__ == "__main__":
    import sys
    if not (len(sys.argv) > 2):
        print "no can do, need more info"
        print """

        contextpyBenchmark.py {activation|runtime} num_layers arg

            activation  run activation bench
            runtime     run runtime bench

            num_layers  number of layers to bench for
            arg         for activation:
                            flat        flat activation
                            nested      nested activation
                        for runtime:
                            standard    run without any layer ideas whatsoever
                            nolayer     run *without* any layer *activated*
                            layer       run *with* num_layers *activated*
        """
        exit(1)
    activation_or_runtime = sys.argv[1] == 'activation' # or runtime
    num_layers = int(sys.argv[2]) #
    arg = sys.argv[3]

    if activation_or_runtime:
        ContextPyLayerActivationBench().run(num_layers, arg)
    else:
        ContextPyMethodBench2().run(num_layers, arg)
