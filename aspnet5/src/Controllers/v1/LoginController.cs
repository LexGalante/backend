using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using src.Services;
using src.ViewModels;

namespace src.Controllers.v1
{
    [Route("api/v1/[controller]")]
    [ApiController]
    [AllowAnonymous]
    public class LoginController : ControllerBase
    {
        private readonly ILogger<LoginController> _logger;
        private readonly AuthService _service;

        public LoginController(ILogger<LoginController> logger, AuthService service)
        {
            _logger = logger;
            _service = service;
        }

        [HttpPost]
        [ProducesResponseType(typeof(JwtViewModel), (int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.Unauthorized)]
        [ProducesResponseType((int)HttpStatusCode.BadRequest)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public async Task<IActionResult> PostAsync([FromBody] LoginViewModel viewModel)
        {
            var token = await _service.AuthenticateAsync(viewModel.Username, viewModel.Password);

            return Ok(new JwtViewModel
            {
                TokenType = "Bearer",
                AccessToken = token
            });
        }
    }

}