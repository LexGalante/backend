using System;

namespace src.Models
{
    public class ApplicationFeature
    {
        public int Id { get; set; }
        public int ApplicationId { get; set; }
        public int EnvironmentId { get; set; }
        public string Name { get; set; }
        public bool Enable { get; set; }
        public DateTime CreatedAt { get; set; }
        public int CreatedBy { get; set; }
        public DateTime UpdatedAt { get; set; }
        public int UpdatedBy { get; set; }

        public Application Application { get; set; }
        public Environment Environment { get; set; }

        public void GenerateName() => Name = Name.Replace(" ", "_").Trim();
    }
}