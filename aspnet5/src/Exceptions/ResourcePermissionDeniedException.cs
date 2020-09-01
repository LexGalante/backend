using System;

namespace src.Exceptions
{
    public class ResourcePermissionDeniedException<T> : Exception
    {
        public ResourcePermissionDeniedException(string message) : base (message)
        {
            
        }
    }
}