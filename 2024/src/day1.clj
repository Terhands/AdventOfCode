(ns day1
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
(def contents (string/split-lines (readContents "src/day1_input.txt")))
;; next up I want to iterate over those contents, and break up each line
;; into a val1 val2 tuple - map works well for this, but we'll need a function
;; that accepts a single value in the call to map, so I need to set up a 
;; to_tuple function here that'll take my string, and split it by N spaces
;; may as well also cast our strings back to integers here while we're
;; at it.
(defn to_tuple [val] (map Integer/parseInt (string/split val #" +")))
;; this is pulling it all together into our mapping function
(defn tups [elements] (map to_tuple elements))
;; This ends up being a list of our two lists - both sorted.
;; we'll use this to let us "zip" the two lists back together
(def sorted_tuples (map sort (apply map vector (tups contents))))
(def zipped_lists (map vector (first sorted_tuples) (second sorted_tuples)))
;; ready to be subtracted, and then finally summed back togther
;; to get our final answer.
(defn subtract [l] (abs (reduce - l)))
(reduce + (map subtract zipped_lists))
(println (reduce + (map subtract zipped_lists)))

;; PART 2
(def p2_contents (string/split-lines (readContents "src/day1_input.txt")))
(def p2_lists (apply map vector (tups p2_contents)))
;; Split apart our two lists, so we can iterate through them independently
;; Going for a strategy of:
;; 1. map onto each element in the left list
;;   2. filter the right list by the current element
;;   3. Get the length, then multiply el by len of the filtered list
;; 4. Sum the resulting data
(defn eq_filter [x] (filter
                     (fn [y] (= x y))
                     (second p2_lists)))
(defn score [x] (* x (count (eq_filter x))))
;; solution to P2: 19678534
(reduce + (map score (first p2_lists)))
