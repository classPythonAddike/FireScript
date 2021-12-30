(begin
    (define radius 100)
    (define pi 3.141592)

    (define r (float radius))
    
    (put "Radius of the sphere is " r " units.")

    (put "Surface Area = " (* 4 pi r r) " sq. units.")
    (put "Volume = " (* (/ 4 3) pi r r r) " cubic units.")
)
