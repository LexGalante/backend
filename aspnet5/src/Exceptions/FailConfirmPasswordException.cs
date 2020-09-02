using System;

namespace src.Exceptions
{
    public class FailConfirmPasswordException : Exception
    {
        public FailConfirmPasswordException() : base("password and confirm password is must be same")
        {
            
        }
    }
}