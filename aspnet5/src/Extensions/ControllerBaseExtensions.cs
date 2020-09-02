using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace src.Extensions
{
    public static class ControllerBaseExtensions
    {
        public static string GetCurrentUserEmail(this ControllerBase controller, IHttpContextAccessor httpContext) => 
            httpContext.HttpContext.User.Identity.Name; 

        public static bool CurrentUserIsAuthenticated(this ControllerBase controller, IHttpContextAccessor httpContext) =>
            httpContext.HttpContext.User.Identity.IsAuthenticated;
    }
}