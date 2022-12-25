(defun find-set-length (str length)
  (loop for i from 0 below (length str)
    do (if
          (equal (length (remove-duplicates (subseq str i (+ i length)))) length)
          (return (+ i length)))))

(defun part1 (str) (print (find-set-length str 4)))

(defun part2 (str) (print (find-set-length str 14)))

(defun solve (str)
  (progn (part1 str) (part2 str)))

(solve (read-line))
