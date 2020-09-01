using System;

namespace src.Exceptions
{
    public class UnauthorizeException : Exception
    {
        public UnauthorizeException(string email) : base("Email/Password is invalid...")
        {
            
        }
    }
}