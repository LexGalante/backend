using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using src.Extensions;
using src.Models;
using src.Services;
using src.ViewModels;

namespace src.Controllers.v1
{
    [Route("api/v1/[controller]")]
    [ApiController]
    [Authorize]
    public class UserController : ControllerBase
    {
        private readonly ILogger<UserController> _logger;
        private readonly UserService _service;
        private readonly IHttpContextAccessor _httpContextAcessor;

        public UserController(ILogger<UserController> logger, UserService service, IHttpContextAccessor httpContextAccessor)
        {
            _logger = logger;
            _service = service;
            _httpContextAcessor = httpContextAccessor;
        }

        [HttpGet]
        [Route("paginate/{page}/{pageSize}")]
        [ProducesResponseType(typeof(List<User>), (int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> PaginateAsync([FromRoute] int page, [FromRoute] int pageSize)
        {
            var users = await _service.PaginateAsync(page, pageSize);

            return Ok(users);
        }

        [HttpGet]
        [Route("/{email}")]
        [ProducesResponseType(typeof(User), (int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> GetByEmailAsync([FromRoute] string email)
        {
            var user = await _service.GetByEmailAsync(email);

            return Ok(user);
        }

        [HttpPatch]
        [Route("change-password")]
        [ProducesResponseType((int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> ChangePasswordAsync([FromBody] ChangePasswordViewModel viewModel)
        {
            var user = await _service.ChangePasswordAsync(this.GetCurrentUserEmail(_httpContextAcessor), viewModel.NewPassword, viewModel.ConfirmPassword);
        
            return Ok();
        }
    }

}