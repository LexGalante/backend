using src.Resources;
using System.Threading.Tasks;
using System.Linq;
using System.Collections;
using Microsoft.EntityFrameworkCore;
using src.Models;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;
using Microsoft.Extensions.Logging;
using src.Exceptions;

namespace src.Services
{
    public class UserService
    {
        private readonly ILogger<UserService> _logger;
        private readonly ApplicationDbContext _context;

        public UserService(ILogger<UserService> logger, ApplicationDbContext context)
        {
            _logger = logger;
            _context = context;
        }

        public async Task<IList<User>> PaginateAsync(int page, int pageSize) =>
            await _context.Users.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync();

        public async Task<User> GetByEmailAsync(string email) =>
            await _context.Users.SingleOrDefaultAsync(x => x.Email == email);

        public async Task<User> CreateAsync(User user)
        {
            user.Active = true;
            user.Password = EncryptPassword(user.Password);
            await _context.Users.AddAsync(user);
            await _context.SaveChangesAsync();

            _logger.LogInformation("New user created {0}", user.Email);

            return user;
        }

        public async Task<bool> ActivateAsync(string email) => await ToggleActiveAsync(email, true);

        public async Task<bool> InactivateAsync(string email) => await ToggleActiveAsync(email, false);

        private async Task<bool> ToggleActiveAsync(string email, bool active) 
        {
            var user = await GetByEmailAsync(email);
            user.Active = active;
            await _context.SaveChangesAsync();

            _logger.LogInformation("user {0} toggle active for {1}", email, active);

            return active;
        }

        public async Task<User> ChangePasswordAsync(string email, string newPassword, string confirmPassword)
        {
            if (newPassword != confirmPassword)
                throw new FailConfirmPasswordException();

            var user = await GetByEmailAsync(email);
            user.Password = EncryptPassword(newPassword);

            _logger.LogInformation("changed the password of user {0}", email);

            return user;
        }

        public string EncryptPassword(string password)
        {
            var crypt = Encoding.UTF8.GetBytes(password);
            crypt = new SHA256Managed().ComputeHash(crypt);

            return Encoding.UTF8.GetString(crypt);
        }
    }
}