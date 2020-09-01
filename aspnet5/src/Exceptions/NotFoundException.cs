using System;

namespace src.Exceptions
{
    public class NotFoundException : Exception
    {
        public NotFoundException(Type model, string message) : base(message)
        {
            
        }
    }
}