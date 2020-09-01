using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using src.Exceptions;
using src.Models;
using src.Resources;

namespace src.Services
{
    public class ApplicationService
    {
        private readonly ILogger<ApplicationService> _logger;
        private readonly ApplicationDbContext _context;
        private readonly UserService _userService;
        private readonly EnvironmentService _environmentService;

        public ApplicationService(ILogger<ApplicationService> logger,
            ApplicationDbContext context,
            UserService userService,
            EnvironmentService environmentService)
        {
            _logger = logger;
            _context = context;
            _userService = userService;
            _environmentService = environmentService;
        }

        public async Task<List<Application>> GetAllByUserAsync(int currentUserId) =>
            await _context.ApplicationUsers
                        .Where(x => x.UserId == currentUserId)
                        .Include(x => x.Application)
                        .Select(x => x.Application)
                        .ToListAsync();

        public async Task<Application> GetByNameAsync(string name, int currentUserId)
        {
            var application = await _context.ApplicationUsers
                                            .Include(x => x.Application)
                                            .Include(x => x.User)
                                            .Where(x => x.UserId == currentUserId && x.Application.Name == name)
                                            .Select(x => x.Application)
                                            .SingleOrDefaultAsync();
            if (application is null)
                throw new ResourcePermissionDeniedException<Application>("Application not found or you doesnt have permission");

            return application;
        }
            
        public async Task<List<ApplicationUser>> GetUsersAsync(string name)
        {
            var application = await _context.Applications.Where(x => x.Name.Equals(name)).Include(x => x.Users).SingleAsync();

            return application?.Users.ToList();
        }
            

        public async Task<List<ApplicationFeature>> GetFeaturesAsync(string name)
        {
            var application = await _context.Applications.Where(x => x.Name.Equals(name)).Include(x => x.Features).SingleAsync();

            return application?.Features.ToList();
        }
        
        public async Task<int> CreateAsync(Application application, int currentUserId)
        {
            application.CreatedAt = DateTime.Now;
            application.CreatedBy = currentUserId;
            application.UpdatedAt = DateTime.Now;
            application.UpdatedBy = currentUserId;
            application.GenerateName();
            while (await _context.Applications.CountAsync(x => x.Name == application.Name) > 0)
                application.GenerateName();
            
            var validator = application.Validate();
            if (!validator.IsValid)
                throw new ValidatorException(validator);

            application.Users.Add(new ApplicationUser()
            {
                UserId = currentUserId
            });
            await _context.AddAsync(application);

            _logger.LogInformation($"new application({application.Name}) created");

            return await _context.SaveChangesAsync();
        }

        public async Task<int> UpdateAsync(string name, Application newValues, int currentUserId)
        {
            var application = await GetByNameAsync(name, currentUserId);
            application.RealName = newValues.RealName;
            application.Model = newValues.Model;
            application.Description = newValues.Description;
            application.Details = newValues.Details;
            application.UpdatedAt = DateTime.Now;
            application.UpdatedBy = currentUserId;

            _logger.LogInformation($"new application({application.Name}) updating");

            return await _context.SaveChangesAsync();
        }

        public async Task<int> ActivateAsync(string name, int currentUserId) => await ToggleActiveAsync(name, true, currentUserId);

        public async Task<int> InactivateAsync(string name, int currentUserId) => await ToggleActiveAsync(name, true, currentUserId);

        public async Task<int> ToggleActiveAsync(string name, bool active, int currentUserId)
        {
            var application = await GetByNameAsync(name, currentUserId);
            application.Active = active;
            application.UpdatedAt = DateTime.Now;
            application.UpdatedBy = currentUserId;

            return await _context.SaveChangesAsync();
        }

        public async Task<int> AddUserAsync(string name, string email, int currentUserId)
        {
            var application = await GetByNameAsync(name, currentUserId);
            var user = await _userService.GetByEmailAsync(name);
            var applicationUser = new ApplicationUser
            {
                ApplicationId = application.Id,
                UserId = user.Id
            };

            await _context.AddAsync(applicationUser);

            return await _context.SaveChangesAsync(); 
        }

        public async Task<int> RemoveUserAsync(string name, string email, int currentUserId)
        {
            var application = await GetByNameAsync(name, currentUserId);
            var user = await _userService.GetByEmailAsync(name);
            var applicationUser = await _context.ApplicationUsers.SingleOrDefaultAsync(x => x.ApplicationId == application.Id && x.UserId == user.Id);
            if (applicationUser != null)
                _context.ApplicationUsers.Remove(applicationUser);

            return await _context.SaveChangesAsync();
        }
    }
}