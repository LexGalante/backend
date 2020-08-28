using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace src.Models.Configurations
{
    public class EnvironmentConfiguration : IEntityTypeConfiguration<Environment>
    {
        public void Configure(EntityTypeBuilder<Environment> builder)
        {
            builder.ToTable("environments");
            builder.HasKey(x => x.Id);

            builder.Property(x => x.Id)
                .HasColumnName("id");

            builder.Property(x => x.Name)
                .HasMaxLength(3)
                .HasColumnName("name");

            builder.Property(x => x.Description)
                .HasMaxLength(250)
                .HasColumnName("description");

            builder.Property(x => x.Active)
                .HasColumnName("active");

            builder.HasMany(x => x.Features)
                .WithOne(x => x.Environment)
                .HasForeignKey(x => x.EnvironmentId)
                .HasConstraintName("application_features_environment_id_fkey");
        }
    }
}