using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace src.Models.Configurations
{
    public class UserConfiguration : IEntityTypeConfiguration<User>
    {
        public void Configure(EntityTypeBuilder<User> builder)
        {
            builder.ToTable("users");
            builder.HasKey(x => x.Id);

            builder.Property(x => x.Id)
                .HasColumnName("id");

            builder.Property(x => x.Email)
                .HasMaxLength(250)
                .HasColumnName("email");

            builder.Property(x => x.Password)
                .HasMaxLength(250)
                .HasColumnName("password");

            builder.HasMany(x => x.Applications)
                .WithOne(x => x.User)
                .HasForeignKey(x => x.UserId)
                .HasConstraintName("application_users_user_id_fkey");
        }
    }
}