(ns day2
  (:gen-class)
  (:require
   [clojure.string :as string]))

(defn readContents [filename]
  ;; read the contents of filename - note filename needs to be prefixed with src
  ;; I should probably pull this out into a shared file that I can just reload for
  ;; each day to make life easier on myself :D
  (def string1 (slurp filename))
  string1)

;; part 1
;; first up, parsing in clojure... split-lines will split apart my
;; file into a list of strings (excluing the newline character)
;; Remember to evaluate this line, or contents wont exist.
(def contents (string/split-lines (readContents "src/day2_input.txt")))
(defn parse_data_to_integers [val] (map Integer/parseInt (string/split val #" +")))
;; this is pulling it all together into our mapping function
(defn parsed_level_reports [elements] (map parse_data_to_integers elements))
;; there must be a better way to do this - partition is putting my "steps" of 2-tuples into a vector
;; in the form ([(x1, y1)], [(x2, y2)], ...) so I'm having to unpack that first layer before I can
;; get at the values.
(defn subtract_tuple [l] (- (first l) (second l)))
(defn compute_level_changes [report] (map subtract_tuple (partition 2 1 report)))
;; compute how our levels are changing
(def level_deltas (map compute_level_changes (parsed_level_reports contents)))
;; Next, reduce the delta sequences to a safe / unsafe classification. We'll call safe = 1/-1, unsafe = 0
;; to make summing the part 1 result easy.
(def MAX_CHANGE 3)
(def UNSAFE 0)
(def POS_SAFE 1)
(def NEG_SAFE -1)

;; here is our safety check - we're safe if:
;; 1. we're always changing in the same direction
;; 2. there is always change
;; 3. the change is never larger than our MAX_CHANGE
;; To "encode" which direction our previous reduction was changing in
;; we'll keep the sign and have a positive "safe" value as well as
;; a negative "safe" value.
(defn safety [x y] 
  ;; unsafe if either delta didn't change
  println(x)
  println(y)
  (if (or (== x 0) (== y 0)) UNSAFE
      ;; unsafe if the changes were too large
    (if (or (> (abs x) MAX_CHANGE) (> (abs y) MAX_CHANGE)) UNSAFE
        (if (and (< x 0) (< y 0)) NEG_SAFE 
            (if (and (> x 0) (> y 0)) POS_SAFE
                UNSAFE))) 
  ))

(defn split_deltas [deltas] (partition 2 1 deltas))
(defn reduce_to_safety_values [lds] (map (fn [l] (reduce safety l)) lds))
(defn is_safe? [x y] (if (or (== x 0) (== y 0)) 0 1))
(reduce + (map (fn [l] (reduce is_safe? l)) (map reduce_to_safety_values (map split_deltas level_deltas))))

;; part 2
;; one of the level deltas _can_ be unsafe, but no more than one
(defn total_safety [x y] (+ (abs x) (abs y)))
(defn required_safety [l] (- (count l) 1))
(defn p2_safety_value [l] (if (>= (reduce total_safety l) (required_safety l)) 1 0))

;; some tests for a sanity check on p2_safety_value
;; (p2_safety_value [0 -1 0 -1]) -> 0
;; (p2_safety_value [-1 -1 0 -1]) -> 1
;; (p2_safety_value [1 1 0 1]) -> 1
;; (p2_safety_value [1 1 1 1]) -> 1

(defn p2_is_safe [l] (reduce total_safety l))
(map split_deltas level_deltas)
(map reduce_to_safety_values (map split_deltas level_deltas))
(map p2_safety_value (map reduce_to_safety_values (map split_deltas level_deltas)))

