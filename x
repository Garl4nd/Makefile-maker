b1.f90(2): error #7002: Error in opening the compiled module file.  Check INCLUDE paths.   [MOD2]
    use mod2
--------^
b1.f90(3): error #7002: Error in opening the compiled module file.  Check INCLUDE paths.   [MOD3]
    use mod3
--------^
b1.f90(4): error #7002: Error in opening the compiled module file.  Check INCLUDE paths.   [MOD23]
    use mod23
--------^
b1.f90(5): error #7002: Error in opening the compiled module file.  Check INCLUDE paths.   [MOD32]
    use mod32
--------^
b1.f90(7): error #6404: This name does not have a type, and must have an explicit type.   [I2]
    print *,i2,i3
------------^
b1.f90(7): error #6404: This name does not have a type, and must have an explicit type.   [I3]
    print *,i2,i3
---------------^
compilation aborted for b1.f90 (code 1)
b2.f90(2): error #7002: Error in opening the compiled module file.  Check INCLUDE paths.   [MOD4]
    use mod4
--------^
b2.f90(8): error #6404: This name does not have a type, and must have an explicit type.   [I4]
        print *,i4,"from b2"
----------------^
b2.f90(13): error #7002: Error in opening the compiled module file.  Check INCLUDE paths.   [MOD3]
    use mod3
--------^
compilation aborted for b2.f90 (code 1)
b3.f90(2): error #7002: Error in opening the compiled module file.  Check INCLUDE paths.   [MOD4]
    use mod4
--------^
b3.f90(8): error #6404: This name does not have a type, and must have an explicit type.   [I4]
        print *,i4,"from b3"
----------------^
b3.f90(13): error #7002: Error in opening the compiled module file.  Check INCLUDE paths.   [MOD2]
    use mod2
--------^
compilation aborted for b3.f90 (code 1)
