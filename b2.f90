module mod2
    use mod4
    implicit none
    integer :: i2=2
    contains 
    subroutine print42()

        print *,i4,"from b2"
    endsubroutine 
endmodule

module mod23
    use mod3
    contains
    subroutine print32()
        print *,i3,"from b2"
    endsubroutine 
endmodule

