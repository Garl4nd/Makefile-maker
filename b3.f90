module mod3
    use mod4
    implicit none
    integer :: i3=2
    contains 
    subroutine print43()

        print *,i4,"from b3"
    endsubroutine 
endmodule

module mod32
    use mod2
    contains
    subroutine print23()
        print *,i2,"from b3"
    endsubroutine 
endmodule
