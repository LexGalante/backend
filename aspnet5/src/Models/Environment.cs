using System.Collections.Generic;

namespace src.Models
{
    public class Environment
    {
        public const string DEVELOPMENT = "dev";
        public const string TESTING = "tes";
        public const string HOMOLOGATION = "hml";
        public const string PRODUCTION = "prd";


        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public bool Active { get; set; }


        public IList<ApplicationFeature> Features { get; set; }
    }
}