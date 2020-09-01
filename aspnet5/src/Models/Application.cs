using System;
using System.Collections.Generic;
using System.Linq;
using FluentValidation;
using FluentValidation.Results;

namespace src.Models
{
    public class Application
    {
        public enum ApplicationModel
        {
            WEB = 1,
            MOB = 2,
            DES = 3
        }

        public int Id { get; set; }
        public string Name { get; set; }
        public string RealName { get; set; }
        public ApplicationModel Model { get; set; }
        public string Description { get; set; }
        public string Details { get; set; }
        public bool Active { get; set; } = true;
        public DateTime CreatedAt { get; set; } = DateTime.Now;
        public int CreatedBy { get; set; }
        public DateTime UpdatedAt { get; set; } = DateTime.Now;
        public int UpdatedBy { get; set; }

        public IList<ApplicationUser> Users { get; set; } = new List<ApplicationUser>();
        public IList<ApplicationFeature> Features { get; set; } = new List<ApplicationFeature>();

        public Application()
        {
            
        }

        public void GenerateName() => Name = RealName.Replace(" ", "_").Trim();

        public ValidationResult Validate() => new ApplicationValidator().Validate(this);
    }

    public class ApplicationValidator : AbstractValidator<Application>
    {
        public ApplicationValidator()
        {
            RuleFor(x => x.RealName)
                .NotNull()
                .MinimumLength(3)
                .MaximumLength(250)
                .WithSeverity(Severity.Error)
                .WithMessage("[REAL_NAME] is mandatory and must between 3 and 250 characteres");

            RuleFor(x => x.Model)
                .NotNull()
                .WithSeverity(Severity.Error)
                .WithMessage("[MODEL] is mandatory and must be 1(WEB), 2(MOB), 3(DES)");

            RuleFor(x => x.Description)
                .NotNull()
                .MinimumLength(10)
                .MaximumLength(250)
                .WithSeverity(Severity.Error)
                .WithMessage("[DESCRIPTION] is mandatory and must between 10 and 250 characteres");

            RuleFor(x => new { x.Id, x.Users })
                .Custom((model, context) => {
                    if(model.Id == 0 && !model.Users.Any())
                        context.AddFailure("[USERS] application must have one users");
                });
        }
    }
}