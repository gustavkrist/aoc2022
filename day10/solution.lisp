(defparameter *cycles* 1)
(defparameter *x* 1)
(defparameter *total* 0)
(defparameter *image* (make-array '(6 40) :initial-element #\space :element-type 'character))

(defun draw-pixel ()
  (let ((pixel (if (<= (1- *x*) (mod (1- *cycles*) 40) (1+ *x*))
                   #\█
                   #\.)))
    (setf (row-major-aref *image* (1- *cycles*)) pixel)))

(defun check-cycles ()
  (draw-pixel)
  (if 
      (= (mod (- *cycles* 20) 40) 0)
      (incf *total* (* *cycles* *x*))))

(defun addx (amount)
  (check-cycles)
  (incf *cycles*)
  (check-cycles)
  (incf *x* amount)
  (incf *cycles*))

(defun noop ()
  (check-cycles)
  (incf *cycles*))

(loop for line = (read-line *standard-input* nil)
      while line
      do (eval (read-from-string (format nil "(~a)" line))))

(format t "~a~%" *total*)

(loop for row below 6
      do (format t "~a~%" (make-array 40 :displaced-to *image* :displaced-index-offset (* row 40) :element-type 'character)))
