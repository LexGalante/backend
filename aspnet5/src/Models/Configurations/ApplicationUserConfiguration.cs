using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace src.Models.Configurations
{
    public class ApplicationUserConfiguration : IEntityTypeConfiguration<ApplicationUser>
    {
        public void Configure(EntityTypeBuilder<ApplicationUser> builder)
        {
            builder.ToTable("application_users");
            builder.HasKey(x => x.Id);

            builder.Property(x => x.Id)
                .HasColumnName("id");

            builder.Property(x => x.ApplicationId)
                .HasColumnName("application_id");

            builder.Property(x => x.UserId)
                .HasColumnName("user_id");

            builder.HasOne(x => x.User)
                .WithMany(x => x.Applications)
                .HasForeignKey(x => x.UserId)
                .HasConstraintName("application_users_user_id_fkey");

            builder.HasOne(x => x.Application)
                .WithMany(x => x.Users)
                .HasForeignKey(x => x.ApplicationId)
                .HasConstraintName("application_users_application_id_fkey");
        }
    }
}