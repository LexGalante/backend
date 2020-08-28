namespace src.Models
{
    public class ApplicationUser
    {
        public int Id { get; set; }
        public int ApplicationId { get; set; }  
        public int UserId { get; set; } 

        public Application Application { get; set; }
        public User User { get; set; }
    }
}