using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using src.Extensions;
using src.Models;
using src.Services;

namespace src.Controllers.v1
{
    [Route("api/v1/[controller]")]
    [ApiController]
    public class ApplicationController : ControllerBase
    {
        private readonly ILogger<ApplicationController> _logger;
        private readonly IHttpContextAccessor _httpContextAcessor;
        private readonly ApplicationService _service;


        public ApplicationController(ILogger<ApplicationController> logger, IHttpContextAccessor httpContextAccessor, ApplicationService service)
        {
            _logger = logger;
            _httpContextAcessor = httpContextAccessor;
            _service = service;
        }

        [HttpGet]
        [ProducesResponseType(typeof(List<Application>), (int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> GetAsync()
        {
            var applications = await _service.GetAllByUserAsync(this.GetCurrentUserEmail(_httpContextAcessor));

            return Ok(applications);
        }

        [HttpGet]
        [Route("/{name}")]
        [ProducesResponseType(typeof(Application), (int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> GetByNameAsync(string name)
        {
            var applications = await _service.GetByNameAsync(name, this.GetCurrentUserEmail(_httpContextAcessor));

            return Ok(applications);
        }

        [HttpPost]
        [ProducesResponseType((int)HttpStatusCode.Created)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> PostAsync([FromBody] Application application)
        {
            await _service.CreateAsync(application, this.GetCurrentUserEmail(_httpContextAcessor));

            return Created(string.Empty, null);
        }

        [HttpPost]
        [Route("/{name}")]
        [ProducesResponseType((int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> PutAsync([FromRoute] string name, [FromBody] Application application)
        {
            await _service.UpdateAsync(name, application, this.GetCurrentUserEmail(_httpContextAcessor));

            return Ok();
        }

        [HttpPatch]
        [Route("/{name}/activate")]
        [ProducesResponseType((int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> ActivateAsync([FromRoute] string name)
        {
            await _service.ActivateAsync(name, this.GetCurrentUserEmail(_httpContextAcessor));

            return Ok();
        }

        [HttpPatch]
        [Route("/{name}/inactivate")]
        [ProducesResponseType((int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> InactivateAsync([FromRoute] string name)
        {
            await _service.InactivateAsync(name, this.GetCurrentUserEmail(_httpContextAcessor));

            return Ok();
        }

        [HttpGet]
        [Route("/{name}/users")]
        [ProducesResponseType(typeof(List<ApplicationUser>),(int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> GetUsersAsync([FromRoute] string name)
        {
            var application = await _service.GetByNameAsync(name, this.GetCurrentUserEmail(_httpContextAcessor));

            return Ok(application.Users);
        }

        [HttpPost]
        [Route("/{name}/users/{user}")]
        [ProducesResponseType((int)HttpStatusCode.Created)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> PostUserAsync([FromRoute] string name, [FromRoute] string user)
        {
            await _service.AddUserAsync(name, user, this.GetCurrentUserEmail(_httpContextAcessor));

            return Created($"/api/v1/application/{name}/users", null);
        }

        [HttpDelete]
        [Route("/{name}/users/{user}")]
        [ProducesResponseType((int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> DeleteUserAsync([FromRoute] string name, [FromRoute] string user)
        {
            await _service.RemoveUserAsync(name, user, this.GetCurrentUserEmail(_httpContextAcessor));

            return Ok();
        }
    }

}