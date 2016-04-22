(in-package :contextl-user)

(eval-when (:compile-toplevel :load-toplevel :execute compile)
  (format t "foo")
  (proclaim '(optimize 
              (safety 0)
              (debug 0)
              (compilation-speed 0)
              (space 0)
              (speed 3))))

(ql:quickload "contextl")

(defstruct timer
  (value (get-internal-real-time))
  (number-of-opps 0))

(defun stop-timer (timer)
  (setf (timer-value timer)
        (- (get-internal-real-time)
           (timer-value timer))))

(defun print-perf-timer (timer)
  (format t "~S ~S Number of Opps: ~S~%"
          (timer-number-of-opps timer)
          (timer-value timer)
          (coerce (/ (timer-number-of-opps timer)
                     (timer-value timer))
                  'float)))

(defconstant +init-size+ 200000)
(defconstant +max-size+ 1000000000)
(defconstant +target-time+ (* internal-time-units-per-second 5.0))

(defmacro deflayers (&rest names)
  `(progn ,@(loop for name in names collect `(deflayer ,name))))

(deflayers l01 l02 l03 l04 l05 l06 l07 l08 l09 l10 l11 l12 l13 l14)

(defmacro defcounters (&rest names)
  `(progn ,@(loop for name in names
                  collect `(declaim (integer ,name))
                  collect `(defparameter ,name 0))))

(defcounters *counter01* *counter02* *counter03* *counter04* *counter05*
             *counter06* *counter07* *counter08* *counter09* *counter10*
             *counter11* *counter12* *counter13* *counter14* *counter15*)

(defun reset-counter ()
  (setf *counter01* 0
        *counter02* 0
        *counter03* 0
        *counter04* 0
        *counter05* 0
        *counter06* 0
        *counter07* 0
        *counter08* 0
        *counter09* 0
        *counter10* 0
        *counter11* 0
        *counter12* 0
        *counter13* 0
        *counter14* 0
        *counter15* 0))

(defmethod no-layer01 ()
  (incf *counter01*))

(defmethod no-layer02 ()
  (incf *counter01*)
  (incf *counter02*))

(defmethod no-layer03 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*))

(defmethod no-layer04 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*))

(defmethod no-layer05 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*)
  (incf *counter05*))

(defmethod no-layer06 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*)
  (incf *counter05*)
  (incf *counter06*))

(defmethod no-layer07 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*)
  (incf *counter05*)
  (incf *counter06*)
  (incf *counter07*))

(defmethod no-layer08 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*)
  (incf *counter05*)
  (incf *counter06*)
  (incf *counter07*)
  (incf *counter08*))

(defmethod no-layer09 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*)
  (incf *counter05*)
  (incf *counter06*)
  (incf *counter07*)
  (incf *counter08*)
  (incf *counter09*))

(defmethod no-layer10 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*)
  (incf *counter05*)
  (incf *counter06*)
  (incf *counter07*)
  (incf *counter08*)
  (incf *counter09*)
  (incf *counter10*))

(defmethod no-layer11 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*)
  (incf *counter05*)
  (incf *counter06*)
  (incf *counter07*)
  (incf *counter08*)
  (incf *counter09*)
  (incf *counter10*)
  (incf *counter11*))

(defmethod no-layer12 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*)
  (incf *counter05*)
  (incf *counter06*)
  (incf *counter07*)
  (incf *counter08*)
  (incf *counter09*)
  (incf *counter10*)
  (incf *counter11*)
  (incf *counter12*))

(defmethod no-layer13 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*)
  (incf *counter05*)
  (incf *counter06*)
  (incf *counter07*)
  (incf *counter08*)
  (incf *counter09*)
  (incf *counter10*)
  (incf *counter11*)
  (incf *counter12*)
  (incf *counter13*))

(defmethod no-layer14 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*)
  (incf *counter05*)
  (incf *counter06*)
  (incf *counter07*)
  (incf *counter08*)
  (incf *counter09*)
  (incf *counter10*)
  (incf *counter11*)
  (incf *counter12*)
  (incf *counter13*)
  (incf *counter14*))

(defmethod no-layer15 ()
  (incf *counter01*)
  (incf *counter02*)
  (incf *counter03*)
  (incf *counter04*)
  (incf *counter05*)
  (incf *counter06*)
  (incf *counter07*)
  (incf *counter08*)
  (incf *counter09*)
  (incf *counter10*)
  (incf *counter11*)
  (incf *counter12*)
  (incf *counter13*)
  (incf *counter14*)
  (incf *counter15*))

(define-layered-function with-layer ())

(define-layered-method with-layer ()
  (incf *counter01*))

(define-layered-method with-layer :in-layer l01 :after ()
  (incf *counter02*))

(define-layered-method with-layer :in-layer l02 :after ()
  (incf *counter03*))

(define-layered-method with-layer :in-layer l03 :after ()
  (incf *counter04*))

(define-layered-method with-layer :in-layer l04 :after ()
  (incf *counter05*))

(define-layered-method with-layer :in-layer l05 :after ()
  (incf *counter06*))

(define-layered-method with-layer :in-layer l06 :after ()
  (incf *counter07*))

(define-layered-method with-layer :in-layer l07 :after ()
  (incf *counter08*))

(define-layered-method with-layer :in-layer l08 :after ()
  (incf *counter09*))

(define-layered-method with-layer :in-layer l09 :after ()
  (incf *counter10*))

(define-layered-method with-layer :in-layer l10 :after ()
  (incf *counter11*))

(define-layered-method with-layer :in-layer l11 :after ()
  (incf *counter12*))

(define-layered-method with-layer :in-layer l12 :after ()
  (incf *counter13*))

(define-layered-method with-layer :in-layer l13 :after ()
  (incf *counter14*))

(define-layered-method with-layer :in-layer l14 :after ()
  (incf *counter15*))

(defun run-method (label function)
  (loop initially (reset-counter)

        with timer
        with consumed-time = 0
        with size = +init-size+

        while (and (< consumed-time +target-time+)
                   (< size +max-size+)) do
        (setq timer (funcall function (* 16 size)))
        (setq consumed-time (timer-value timer))
        (setf (timer-number-of-opps timer) (* 16 size))
        (setq size (* 2 size))

        finally (print label) (print-perf-timer timer)))

(defmacro nol (name)
  `(lambda (repeat-count)
     (let ((timer (make-timer)))
       (loop repeat repeat-count do (,name))
       (stop-timer timer)
       timer)))

(defmacro lact (name &rest layers)
  `(lambda (repeat-count)
     (with-active-layers ,layers
       (let ((timer (make-timer)))
         (loop repeat repeat-count do (,name))
         (stop-timer timer)
         timer))))

(defun run ()
  (run-method "ContextL:Method:NoLayer:1" (nol no-layer01))
  (run-method "ContextL:Method:NoLayer:2" (nol no-layer02))
  (run-method "ContextL:Method:NoLayer:3" (nol no-layer03))
  (run-method "ContextL:Method:NoLayer:4" (nol no-layer04))
  (run-method "ContextL:Method:NoLayer:5" (nol no-layer05))
  (run-method "ContextL:Method:NoLayer:6" (nol no-layer06))
  (run-method "ContextL:Method:NoLayer:7" (nol no-layer07))
  (run-method "ContextL:Method:NoLayer:8" (nol no-layer08))
  (run-method "ContextL:Method:NoLayer:9" (nol no-layer09))
  (run-method "ContextL:Method:NoLayer:10" (nol no-layer10))
;  (run-method "ContextL:Method:NoLayer:11" (nol no-layer11))
;  (run-method "ContextL:Method:NoLayer:12" (nol no-layer12))
;  (run-method "ContextL:Method:NoLayer:13" (nol no-layer13))
;  (run-method "ContextL:Method:NoLayer:14" (nol no-layer14))
;  (run-method "ContextL:Method:NoLayer:15" (nol no-layer15))
  
  (run-method "ContextL:Method:Layer" (nol with-layer))
  (run-method "ContextL:Method:Layer:1" (lact with-layer l01))
  (run-method "ContextL:Method:Layer:2" (lact with-layer l01 l02))
  (run-method "ContextL:Method:Layer:3" (lact with-layer l01 l02 l03))
  (run-method "ContextL:Method:Layer:4" (lact with-layer l01 l02 l03 l04))
  (run-method "ContextL:Method:Layer:5" (lact with-layer l01 l02 l03 l04 l05))
  (run-method "ContextL:Method:Layer:6" (lact with-layer l01 l02 l03 l04 l05 l06))
  (run-method "ContextL:Method:Layer:7" (lact with-layer l01 l02 l03 l04 l05 l06 l07))
  (run-method "ContextL:Method:Layer:8" (lact with-layer l01 l02 l03 l04 l05 l06 l07 l08))
  (run-method "ContextL:Method:Layer:9" (lact with-layer l01 l02 l03 l04 l05 l06 l07 l08 l09))
  (run-method "ContextL:Method:Layer:10" (lact with-layer l01 l02 l03 l04 l05 l06 l07 l08 l09 l10))
;  (run-method "ContextL:Method:Layer:11" (lact with-layer l01 l02 l03 l04 l05 l06 l07 l08 l09 l10 l11))
;  (run-method "ContextL:Method:Layer:12" (lact with-layer l01 l02 l03 l04 l05 l06 l07 l08 l09 l10 l11 l12))
;  (run-method "ContextL:Method:Layer:13" (lact with-layer l01 l02 l03 l04 l05 l06 l07 l08 l09 l10 l11 l12 l13))
;  (run-method "ContextL:Method:Layer:14" (lact with-layer l01 l02 l03 l04 l05 l06 l07 l08 l09 l10 l11 l12 l13 l14))

  (print "End Method Benchmark"))

(define-layered-function m1 ())
(define-layered-function m2 ())
(define-layered-function m3 ())
(define-layered-function m4 ())
(define-layered-function m5 ())

(define-layered-method m1 ()
  (incf *counter01*))

(define-layered-method m2 ()
  (incf *counter02*))

(define-layered-method m3 ()
  (incf *counter03*))

(define-layered-method m4 ()
  (incf *counter04*))

(define-layered-method m5 ()
  (incf *counter05*))

(define-layered-method m1 :in-layer l01 ()
  (incf *counter01*))

(define-layered-method m2 :in-layer l01 ()
  (incf *counter02*))

(define-layered-method m3 :in-layer l01 ()
  (incf *counter03*))

(define-layered-method m4 :in-layer l01 ()
  (incf *counter04*))

(define-layered-method m5 :in-layer l01 ()
  (incf *counter05*))

(define-layered-method m1 :in-layer l02 ()
  (incf *counter01*))

(define-layered-method m2 :in-layer l02 ()
  (incf *counter02*))

(define-layered-method m3 :in-layer l02 ()
  (incf *counter03*))

(define-layered-method m4 :in-layer l02 ()
  (incf *counter04*))

(define-layered-method m5 :in-layer l02 ()
  (incf *counter05*))

(define-layered-method m1 :in-layer l03 ()
  (incf *counter01*))

(define-layered-method m2 :in-layer l03 ()
  (incf *counter02*))

(define-layered-method m3 :in-layer l03 ()
  (incf *counter03*))

(define-layered-method m4 :in-layer l03 ()
  (incf *counter04*))

(define-layered-method m5 :in-layer l03 ()
  (incf *counter05*))

(define-layered-method m1 :in-layer l04 ()
  (incf *counter01*))

(define-layered-method m2 :in-layer l04 ()
  (incf *counter02*))

(define-layered-method m3 :in-layer l04 ()
  (incf *counter03*))

(define-layered-method m4 :in-layer l04 ()
  (incf *counter04*))

(define-layered-method m5 :in-layer l04 ()
  (incf *counter05*))

(define-layered-method m1 :in-layer l05 ()
  (incf *counter01*))

(define-layered-method m2 :in-layer l05 ()
  (incf *counter02*))

(define-layered-method m3 :in-layer l05 ()
  (incf *counter03*))

(define-layered-method m4 :in-layer l05 ()
  (incf *counter04*))

(define-layered-method m5 :in-layer l05 ()
  (incf *counter05*))

(defun run-reference (label)
  (loop initially (reset-counter)

        with timer
        with consumed-time = 0
        with size = +init-size+

        while (and (< consumed-time +target-time+)
                   (< size +max-size+)) do
        (setq timer (make-timer))
        (loop repeat (* 16 size) do (m1) (m2) (m3) (m4) (m5))
        (stop-timer timer)
        (setq consumed-time (timer-value timer))
        (setf (timer-number-of-opps timer) (* 16 size))
        (setq size (* 2 size))

        finally (print label) (print-perf-timer timer)))

(defun run-method-with-nested-layers1 (label)
  (loop initially (reset-counter)

        with timer
        with consumed-time = 0
        with size = +init-size+

        while (and (< consumed-time +target-time+)
                   (< size +max-size+)) do
        (setq timer (make-timer))
        (loop repeat (* 16 size) do
              (with-active-layers (l01)
                (m1) (m2) (m3) (m4) (m5)))
        (stop-timer timer)
        (setq consumed-time (timer-value timer))
        (setf (timer-number-of-opps timer) (* 16 size))
        (setq size (* 2 size))

        finally (print label) (print-perf-timer timer)))

(defun run-method-with-nested-layers2 (label)
  (loop initially (reset-counter)

        with timer
        with consumed-time = 0
        with size = +init-size+

        while (and (< consumed-time +target-time+)
                   (< size +max-size+)) do
        (setq timer (make-timer))
        (loop repeat (* 16 size) do
              (with-active-layers (l01)
                (m1)
                (with-active-layers (l02)
                  (m2) (m3) (m4) (m5))))
        (stop-timer timer)
        (setq consumed-time (timer-value timer))
        (setf (timer-number-of-opps timer) (* 16 size))
        (setq size (* 2 size))

        finally (print label) (print-perf-timer timer)))

(defun run-method-with-nested-layers3 (label)
  (loop initially (reset-counter)

        with timer
        with consumed-time = 0
        with size = +init-size+

        while (and (< consumed-time +target-time+)
                   (< size +max-size+)) do
        (setq timer (make-timer))
        (loop repeat (* 16 size) do
              (with-active-layers (l01)
                (m1)
                (with-active-layers (l02)
                  (m2)
                  (with-active-layers (l03)
                    (m3) (m4) (m5)))))
        (stop-timer timer)
        (setq consumed-time (timer-value timer))
        (setf (timer-number-of-opps timer) (* 16 size))
        (setq size (* 2 size))

        finally (print label) (print-perf-timer timer)))

(defun run-method-with-nested-layers4 (label)
  (loop initially (reset-counter)

        with timer
        with consumed-time = 0
        with size = +init-size+

        while (and (< consumed-time +target-time+)
                   (< size +max-size+)) do
        (setq timer (make-timer))
        (loop repeat (* 16 size) do
              (with-active-layers (l01)
                (m1)
                (with-active-layers (l02)
                  (m2)
                  (with-active-layers (l03)
                    (m3)
                    (with-active-layers (l04)
                      (m4) (m5))))))
        (stop-timer timer)
        (setq consumed-time (timer-value timer))
        (setf (timer-number-of-opps timer) (* 16 size))
        (setq size (* 2 size))

        finally (print label) (print-perf-timer timer)))

(defun run-method-with-nested-layers5 (label)
  (loop initially (reset-counter)

        with timer
        with consumed-time = 0
        with size = +init-size+

        while (and (< consumed-time +target-time+)
                   (< size +max-size+)) do
        (setq timer (make-timer))
        (loop repeat (* 16 size) do
              (with-active-layers (l01)
                (m1)
                (with-active-layers (l02)
                  (m2)
                  (with-active-layers (l03)
                    (m3)
                    (with-active-layers (l04)
                      (m4)
                      (with-active-layers (l05)
                        (m5)))))))
        (stop-timer timer)
        (setq consumed-time (timer-value timer))
        (setf (timer-number-of-opps timer) (* 16 size))
        (setq size (* 2 size))

        finally (print label) (print-perf-timer timer)))

(defun run2 ()
  (print "Start WITH Benchmark")

  (run-reference "ContextL:WithNested:Layer:0")
  (run-method-with-nested-layers1 "ContextL:WithNested:Layer:1")
  (run-method-with-nested-layers2 "ContextL:WithNested:Layer:2")
  (run-method-with-nested-layers3 "ContextL:WithNested:Layer:3")
  (run-method-with-nested-layers4 "ContextL:WithNested:Layer:4")
  (run-method-with-nested-layers5 "ContextL:WithNested:Layer:5")

  (print "End WITH Benchmark"))

