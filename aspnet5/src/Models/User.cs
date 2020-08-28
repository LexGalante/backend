using FluentValidation;
using FluentValidation.Results;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace src.Models
{
    public class User
    {
        public int Id { get; set; }
        public string Email { get; set; }
        public string Password { get; set; }
        public bool Active { get; set; }

        public IList<ApplicationUser> Applications { get; set; }

        public ValidationResult Validate() => new UserValidator().Validate(this);
    }

    public class UserValidator : AbstractValidator<User>
    {
        private readonly Regex regex = new Regex(
            @"^(?!.*([A-Za-z0-9]))(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,15}$",
            RegexOptions.Compiled
        );

        public UserValidator()
        {
            RuleFor(x => x.Email)
                .NotNull()
                .EmailAddress()
                .WithSeverity(Severity.Error)
                .WithMessage("[EMAIL] must required and a valid email");

            RuleFor(x => x.Password)
                .NotNull()
                .WithSeverity(Severity.Error)
                .WithMessage("[PASSWORD] must required");

            RuleFor(x => new { x.Id, x.Password})
                .Custom((user, context) => {
                    if (user.Id == 0 && !regex.IsMatch(user.Password))
                        context.AddFailure("[PASSWORD]", 
                            "must constains between 8 and 15 characters, upper, lower, special characters");
                });
        }
    }
}