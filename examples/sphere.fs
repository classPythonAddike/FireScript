(begin
    (define pi 3.141592)

    (print "Enter the radius of the sphere: ")

    (define radius "")
    (get radius)
    (define r (float radius))
    
    (put "Radius of the sphere is " r " units.")
    (put "Surface Area = " (* 4.0 pi r r) " sq. units.")
    (put "Volume = " (* (/ 4.0 3.0) pi r r r) " cubic units.")
)
