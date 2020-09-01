using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;
using src.Exceptions;
using src.Models;
using src.Resources;

namespace src.Services
{
    public class AuthService
    {
        private readonly AuthenticationConfiguration _configuration;
        private readonly ILogger<AuthService> _logger;
        private readonly UserService _service;

        public AuthService(IOptions<AuthenticationConfiguration> options, ILogger<AuthService> logger, UserService service)
        {
            _configuration = options.Value;
            _logger = logger;
            _service = service;
        }

        public async Task<string> AuthenticateAsync(string email, string password)
        {
            var user = await _service.GetByEmailAsync(email);
            if (user is null || user.Password != _service.EncryptPassword(password))
                throw new UnauthorizeException(email);

            return GenerateToken(user);
        }

        private string GenerateToken(User user)
        {
            var tokenHandler = new JwtSecurityTokenHandler();
            byte[] key = Encoding.ASCII.GetBytes(_configuration.SecretKey);

            var securityToken = new SecurityTokenDescriptor
            {
                Subject = new ClaimsIdentity(new Claim[]
                {
                    new Claim("id", user.Id.ToString()),
                    new Claim("email", user.Email),
                }),
                Expires = DateTime.UtcNow.AddMinutes(_configuration.MinutesToExpire),
                SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
            };

            var tokenDescriptor = tokenHandler.CreateToken(securityToken);
            
            return tokenHandler.WriteToken(tokenDescriptor);
        }
    }
}