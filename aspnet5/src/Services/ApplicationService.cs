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

        public async Task<List<Application>> GetAllByUserAsync(string author)
        {
            var currentUser = _userService.GetByEmailAsync(author);

            return await _context.ApplicationUsers
                        .Where(x => x.UserId == currentUser.Id)
                        .Include(x => x.Application)
                        .Select(x => x.Application)
                        .ToListAsync();
        }
            

        public async Task<Application> GetByNameAsync(string name, string author)
        {
            var currentUser = _userService.GetByEmailAsync(author);

            var application = await _context.ApplicationUsers
                                            .Include(x => x.Application)
                                            .Include(x => x.User)
                                            .Where(x => x.UserId == currentUser.Id && x.Application.Name == name)
                                            .Select(x => x.Application)
                                            .SingleOrDefaultAsync();
            if (application is null)
                throw new ResourcePermissionDeniedException<Application>("Application not found or you doesnt have permission");

            return application;
        }

        public async Task<Application> GetByNameAsync(string name, User currentUser)
        {
            var application = await GetByNameAsync(name, currentUser.Id);
            if (application is null)
                throw new ResourcePermissionDeniedException<Application>("Application not found or you doesnt have permission");

            return application;
        }

        private async Task<Application> GetByNameAsync(string name, int currentUserId) => 
            await _context.ApplicationUsers
                            .Include(x => x.Application)
                            .Include(x => x.User)
                            .Where(x => x.UserId == currentUserId && x.Application.Name == name)
                            .Select(x => x.Application)
                            .SingleOrDefaultAsync();
            
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
        
        public async Task<int> CreateAsync(Application application, string author)
        {
            var currentUser = _userService.GetByEmailAsync(author);

            application.CreatedAt = DateTime.Now;
            application.CreatedBy = currentUser.Id;
            application.UpdatedAt = DateTime.Now;
            application.UpdatedBy = currentUser.Id;
            application.GenerateName();
            while (await _context.Applications.CountAsync(x => x.Name == application.Name) > 0)
                application.GenerateName();
            
            var validator = application.Validate();
            if (!validator.IsValid)
                throw new ValidatorException(validator);

            application.Users.Add(new ApplicationUser()
            {
                UserId = currentUser.Id
            });
            await _context.AddAsync(application);

            _logger.LogInformation($"new application({application.Name}) created");

            return await _context.SaveChangesAsync();
        }

        public async Task<int> UpdateAsync(string name, Application newValues, string author)
        {
            var currentUser = await _userService.GetByEmailAsync(author);

            var application = await GetByNameAsync(name, currentUser);
            application.RealName = newValues.RealName;
            application.Model = newValues.Model;
            application.Description = newValues.Description;
            application.Details = newValues.Details;
            application.UpdatedAt = DateTime.Now;
            application.UpdatedBy = currentUser.Id;

            _logger.LogInformation($"new application({application.Name}) updating");

            return await _context.SaveChangesAsync();
        }

        public async Task<int> ActivateAsync(string name, string author) => await ToggleActiveAsync(name, true, author);

        public async Task<int> InactivateAsync(string name, string author) => await ToggleActiveAsync(name, true, author);

        public async Task<int> ToggleActiveAsync(string name, bool active, string author)
        {
            var currentUser = await _userService.GetByEmailAsync(author);
            var application = await GetByNameAsync(name, currentUser);
            application.Active = active;
            application.UpdatedAt = DateTime.Now;
            application.UpdatedBy = currentUser.Id;

            return await _context.SaveChangesAsync();
        }

        public async Task<int> AddUserAsync(string name, string email, string author)
        {
            var currentUser = await _userService.GetByEmailAsync(author);
            var application = await GetByNameAsync(name, currentUser);
            var user = await _userService.GetByEmailAsync(name);
            var applicationUser = new ApplicationUser
            {
                ApplicationId = application.Id,
                UserId = user.Id
            };

            await _context.AddAsync(applicationUser);

            return await _context.SaveChangesAsync(); 
        }

        public async Task<int> RemoveUserAsync(string name, string email, string author)
        {
            var currentUser = await _userService.GetByEmailAsync(author);
            var application = await GetByNameAsync(name, currentUser);
            var user = await _userService.GetByEmailAsync(name);
            var applicationUser = await _context.ApplicationUsers.SingleOrDefaultAsync(x => x.ApplicationId == application.Id && x.UserId == user.Id);
            if (applicationUser != null)
                _context.ApplicationUsers.Remove(applicationUser);

            return await _context.SaveChangesAsync();
        }

        public async Task<int> AddFeature(string name, string environment_name, string feature_name, bool enable, string author)
        {
            var currentUser = await _userService.GetByEmailAsync(author);
            var application = await GetByNameAsync(name, currentUser);
            var environment = await _environmentService.GetByName(name);

            var applicationFeature = new ApplicationFeature
            {
                ApplicationId = application.Id,
                EnvironmentId = environment.Id,
                Name = feature_name.Replace(" ", "_").ToLower(),
                Enable = enable,
                CreatedAt = DateTime.Now,
                CreatedBy = currentUser.Id,
                UpdatedAt = DateTime.Now,
                UpdatedBy = currentUser.Id
            };

            await _context.ApplicationFeatures.AddAsync(applicationFeature);

            _logger.LogInformation($"new feature({feature_name}) adding into application({name})");

            return await _context.SaveChangesAsync();
        }

        public async Task<int> RemoveFeature(string name, string feature_name, string author)
        {
            var currentUser = await _userService.GetByEmailAsync(author);
            var application = await GetByNameAsync(name, currentUser);
            var applicationFeature = await _context.ApplicationFeatures.SingleOrDefaultAsync(x => x.ApplicationId == application.Id && x.Name.Equals(feature_name));

            _context.ApplicationFeatures.Remove(applicationFeature);

            _logger.LogInformation($"remove feature({feature_name}) into application({name})");

            return await _context.SaveChangesAsync();
        }

        public async Task<int> ActivateFeatureAsync(string name, string environment_name, string feature_name, string author) => 
            await ToggleFeatureEnableAsync(name, environment_name, feature_name, true, author);

        public async Task<int> InactivateFeatureAsync(string name, string environment_name, string feature_name, string author) => 
            await ToggleFeatureEnableAsync(name, environment_name, feature_name, true, author);

        public async Task<int> ToggleFeatureEnableAsync(string name, string environment_name, string feature_name, bool enable, string author) 
        {
            var currentUser = await _userService.GetByEmailAsync(author);
            var application = await GetByNameAsync(name, currentUser);
            var environment = await _environmentService.GetByName(environment_name);
            var applicationFeature = await _context.ApplicationFeatures
                        .SingleOrDefaultAsync(x => 
                            x.ApplicationId == application.Id &&
                            x.Name.Equals(feature_name) &&
                            x.EnvironmentId == environment.Id
                        );
            applicationFeature.Enable = enable;
            applicationFeature.UpdatedAt = DateTime.Now;
            applicationFeature.UpdatedBy = currentUser.Id;

            _context.ApplicationFeatures.Update(applicationFeature);

            _logger.LogInformation($"toggle feature({feature_name}) for({enable}) into application({name})");

            return await _context.SaveChangesAsync();
        }

        public async Task<int> ActivateAllFeaturesAsync(string name, string feature_name, string author) =>
            await ToggleAllFeaturesAsync(name, feature_name, true, author);

        public async Task<int> InactivateAllFeaturesAsync(string name, string feature_name, string author) =>
            await ToggleAllFeaturesAsync(name, feature_name, false, author);

        public async Task<int> ToggleAllFeaturesAsync(string name, string feature_name, bool enable, string author) 
        {
            var currentUser = await _userService.GetByEmailAsync(author);
            var application = await GetByNameAsync(name, currentUser.Id);
            var applicationFeatures = await _context.ApplicationFeatures
                        .Where(x => x.ApplicationId == application.Id && x.Name.Equals(feature_name))
                        .ToListAsync();
            foreach(var applicationFeature in applicationFeatures)
            {
                applicationFeature.Enable = enable;
                applicationFeature.UpdatedAt = DateTime.Now;
                applicationFeature.UpdatedBy = currentUser.Id;

                _context.ApplicationFeatures.Update(applicationFeature);

                _logger.LogInformation($"toggle feature({feature_name}) for({enable}) into application({name})");
            }

            return await _context.SaveChangesAsync();
        }
    }
}