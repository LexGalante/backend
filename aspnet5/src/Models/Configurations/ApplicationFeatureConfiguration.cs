using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace src.Models.Configurations
{
    public class ApplicationFeatureConfiguration : IEntityTypeConfiguration<ApplicationFeature>
    {
        public void Configure(EntityTypeBuilder<ApplicationFeature> builder)
        {
            builder.ToTable("application_features");
            builder.HasKey(x => x.Id);

            builder.Property(x => x.Id)
                .HasColumnName("id");

            builder.Property(x => x.ApplicationId)
                .HasColumnName("application_id");

            builder.Property(x => x.EnvironmentId)
                .HasColumnName("environment_id");

            builder.Property(x => x.Name)
                .HasColumnName("name");

            builder.Property(x => x.Enable)
                .HasColumnName("enable");

            builder.Property(x => x.CreatedAt)
                .HasColumnName("created_at");

            builder.Property(x => x.CreatedBy)
                .HasColumnName("created_by");

            builder.Property(x => x.UpdatedAt)
                .HasColumnName("updated_at");

            builder.Property(x => x.UpdatedBy)
                .HasColumnName("updated_by");

            builder.HasOne(x => x.Environment)
                .WithMany(x => x.Features)
                .HasForeignKey(x => x.EnvironmentId)
                .HasConstraintName("application_features_environment_id_fkey");

            builder.HasOne(x => x.Application)
                .WithMany(x => x.Features)
                .HasForeignKey(x => x.EnvironmentId)
                .HasConstraintName("application_features_application_id_fkey");
        }
    }
}