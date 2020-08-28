using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace src.Models.Configurations
{
    public class ApplicationConfiguration : IEntityTypeConfiguration<Application>
    {
        public void Configure(EntityTypeBuilder<Application> builder)
        {
            builder.ToTable("applications");
            builder.HasKey(x => x.Id);

            builder.Property(x => x.Id)
                .HasColumnName("id");

            builder.Property(x => x.Name)
                .HasColumnName("name");

            builder.Property(x => x.RealName)
                .HasColumnName("real_name");

            builder.Property(x => x.Model)
                .HasColumnName("model");

            builder.Property(x => x.Description)
                .HasColumnName("description");

            builder.Property(x => x.Details)
                .HasColumnName("details");

            builder.Property(x => x.Active)
                .HasColumnName("active");

            builder.Property(x => x.CreatedAt)
                .HasColumnName("created_at");

            builder.Property(x => x.CreatedBy)
                .HasColumnName("created_by");

            builder.Property(x => x.UpdatedAt)
                .HasColumnName("updated_at");

            builder.Property(x => x.UpdatedBy)
                .HasColumnName("updated_by");

            builder.HasMany(x => x.Users)
                .WithOne(x => x.Application)
                .HasForeignKey(x => x.ApplicationId)
                .HasConstraintName("application_users_user_id_fkey");

            builder.HasMany(x => x.Features)
                .WithOne(x => x.Application)
                .HasForeignKey(x => x.ApplicationId)
                .HasConstraintName("application_features_application_id_fkey");
        }
    }
}