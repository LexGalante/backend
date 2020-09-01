using System;
using System.Linq;
using FluentValidation.Results;

namespace src.Exceptions
{
    public class ValidatorException : Exception
    {
        public ValidatorException(ValidationResult validationResult) : base(string.Join(", ", validationResult.Errors.Select(x => x.ErrorMessage)))
        {
            
        }
    }
}