using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using src.Models;
using src.Resources;

namespace src.Services
{
    public class EnvironmentService
    {
        private readonly ILogger<EnvironmentService> _logger;
        private readonly ApplicationDbContext _context;

        public EnvironmentService(ILogger<EnvironmentService> logger, ApplicationDbContext context)
        {
            _logger = logger;
            _context = context;
        }

        public async Task<IList<Environment>> GetAllAsync() => 
            await _context.Environments.ToListAsync();

        public async Task<Environment> GetByName(string name) =>
            await _context.Environments.SingleOrDefaultAsync(x => x.Name == name);
    }
}