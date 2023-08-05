(import hashlib cloudpickle requests math [anarcute[*]] asyncio aiohttp
        os psutil [pegasi.req[*]] [pandas :as pd] base64)



(defn mem[] (-> os (.getpid) psutil.Process (.memory-info) (. rss)))
(defn dumps[x] (-> x cloudpickle.dumps base64.b64encode))
(defn loads[x] (-> x base64.b64decode cloudpickle.loads))
(defn hash[key]
  (-> key (.encode "utf-8") hashlib.sha224 (.hexdigest)))
(defclass Dash[object]
  
  (defn --init--[self key &optional [api "http://0.0.0.0:8080/cloudpickle/"]]
    
    (setv self.key key
          
          self.api api
          self.hash (hash key)
          ))
  (defn loads[self x] (loads x))
  (defn dumps[self x] (dumps x));decide out or in
  
  
  
  
  (defn legit[self] (self.run (fn[] {"code" 200 "status" "OK"})))
  (defn run[self f &optional [args []] [kwargs {}][star True][pickled False] [load False] [save False][test False][requirements None]] 
    (do 
      (setv f (if pickled f (self.dumps f)))
      (setv r (-> (requests.post self.api :json {"f" f "args" (self.dumps (if star args [args])) "kwargs" (self.dumps kwargs)
                                                  "save" save "load" load "test" test "requirements" None
                                                  "hash" self.hash}) 
                  ))
      (try (loads r.text) (except[Exception] r.text))
      
      ))
  (defn upload[f name] (run f :save name :test True))
  (defn download[name] (run None :load name :test True))
  (defn map[self f args &optional [processes 80] [star False][requirements []]]
    (if (and processes (> (len args) processes))
      (do (+ (self.map f (get args (slice 0 processes)) processes star requirements)
             (self.map f (get args (slice processes None)) processes star requirements)))
      (do (setv f (self.dumps f))
          (setv urls (* (len args) [self.api])
                params (list (map (fn[a]{"f" f "args" (self.dumps (if star a [a]))
                                         "hash" self.hash "requirements" (self.dumps requirements)}) args)))
          
          (setv r (get_map urls :json params))
          (list (map (fn[x](try (loads x) (except[Exception]{"status" "error" "message" x}))) r))))
    
    )
  
  
  
  (defn *map[self &rest args &kwargs kwargs] (self.map #*args #**kwargs :star True))
  (setv starmap *map)
  (defn filter[self f arr &rest args &kwargs kwargs]
    (setv res (self.map f arr #*args #**kwargs))
    (as-> (list (zip arr res)) it (filter last it) (map first it) (list it))))
