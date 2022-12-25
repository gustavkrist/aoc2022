(defvar *stream* (read-line))

(defun range (stop &key (start 0) (step 1))
  (loop for n from start below stop by step
        collect n))

(defun index-nested-list (i arglist)
  (list (list (nth i arglist))))

(defun list-first-element (arglist)
  (concatenate 'list (index-nested-list 0 arglist) (nthcdr 1 arglist)))

(defun make-set (sequence)
  (reduce #'(lambda (x y) (adjoin y x)) (list-first-element sequence)))

(defun find-set-length (length)
  (loop for i in (range (length *stream*))
    do (if
          (equal (length (make-set (coerce  (subseq *stream* i (+ i length)) 'list))) length)
          (progn (print (+ i length))
                 (return))) ))

(defun part1 () (find-set-length 4))

(defun part2 () (find-set-length 14))

(progn (part1) (part2))
