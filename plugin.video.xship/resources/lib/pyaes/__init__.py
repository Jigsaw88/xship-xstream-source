
import zlib, base64
exec(zlib.decompress(base64.b64decode(zlib.decompress(base64.b64decode('eNoNVjWC5AAMe1CKMBVXhHHC3IWZOa+/rd1IliWrNFZxgEuLONqwNsAteNmiS5e1smbmG3GjQ+zbNAXG6Fpom4k8p0iALi1tMueNd8G4RGESz6LEEpwkLLzj3eKUx/wK1DcluA5COy5O9/QL/7DVJujy8q3erno5D5GO1or9DAmffeh8wMsQAHnAHy6cmQjqCKzFsClrO8uLWQFxwkmwEutjopft/Jaqdo+ajXCNCkH3uCGdurL7DSEUhdieLmg0PdjLP2uUcDJ6wf2oCekR4vdPsOrqZSLMH4q0yA46X9GwrItKhJM/8kQIXuSnpw5YQRvDUwO5mSBx1fzMTx1MYTRqkJgNMBYu6NB7EQdLLkNkVQDAA5bhlryxOODVHHSJZUWEcztFcdNaES+FytPC/GiYOypyD2cqoaWgNAwS+eFtbo7BRPaoJaNatd0n56gwoEcVGQH7fJG4GKWkrp4atJ6H0W5vElYrHp/OcGuUZcEjMVrPC7C0otEHDXhUoaORXgDIdYwoRKlq1UUOySNgrlw1kYkb6IH3A5SXoknRFl/K5Z7DiXaI0dpg5jgAiq7WFehOv+yDfF8kWl8W+pm0anHGmf1kFKx+6Ue6q9RHakSRcYVCgeHoAQc0GU5HIOlzQuXguFPB/enP0YcA2ExfbPS35Cp8gXXqvDLIlM8z0iu8hqCj/MTdDq7TdPBSaBynC6AraCLREYoawcu0yABFrQxWL1y8eJCyALx3CNG6iYNvF7xK1qzwaWDKJGPwiC+wKgR85PfoicDOwUxO6+UALZBCfIey9867xIG2BfGJBZ2cZv46n3vhqvWx41X4OyGIRz/BPvr2YW0f5e6De/gTBazGIWaKLS8QmDSGJPswC4oqpC0vOFNAxv6wkvIN0hkZXl8MeTSYVfIEag1MROSKRhk1UPL5otBFLyOTKOP5YPxQkNHY4ejXA1CAHOAMeAD90UbggvBSSAg4iGKfLAW+tqEH1yuYxksglol9/Mh4H4TwI6wpp4jtrvLraidgly9gSstrSAAHlPFqEkH2kYq51sN7yxKirO5reMlTZt+CTkuUf0iu4vYLJtYqkvG1sk8RWdP8/NCyAasVPo2/A9/8XCEmkPQ4kiPAZeithaimSQVJzA3TK22A6qIbEaL+bMohImCiNFYY1Nl1WHptJjwCSSlRC26OVXhSRzU69V3RyWuBTJVe3U1ZfIHllfzQlwmq7Z2GSyr54s3fv/43DmjKqryxZx++mmb61Qdkv42+CpHYFTaZ2684/yH/Hky1bfsy00ciWoYOyXsIm0KRPR8WslhDXWG6c/2BreN+rXzmdRJ9ueHuAay2IGiEf/uxzYjSMiy6rzoSdKVySiPWy7qEeLTf7PfSHTh5e5EuQHD360jSexZ2jA9TJn8267lPOfGSvXV0kjyU/mYsAtsJ+DU6gUpzYyQqdoReUTEE/uRnozbcG/bAEz/oVHjAYUvMSPTEZ8JRGjnzXeN8XOpfx/z4M1UUDRtnsBCcWbHmnXmCZFT6PTXtMtlH7/F3pk93wkkhNt2xz2LnxYboMIl+JHOVxzJucVQzm9clT3D8SRJ3UTr8fmfB29SUPj1SgvVnZQyJv2M6Y/Hsur+bk3IvCZQgqPmduuwQp+0T3NYoTpEuOsdelxv5hytjiJySnNlzqOgNgnO5hTWzg5ZRcFJGGh5HEEkrcNcJnDiWpr73QW7xn12y61kx+TSvHP4y8pC0QNJxBCoQhfuj9oSh+Jf9PnS79xRfbusqOVm+28yyW0tS+sEvx9A7qYrn9WQOGK9Av4E11c5uDlHiUJtcE9M1+c/t4RHhCA2wTtG1xgKafZfSpc6WpFQ4rpgfNE7MvcrU6rFW1LxtI4IvwsVYjH6IP5OHhVe9nKeuiF8g1XCfAvZuF0V9YCje+Sbhh4f8uv2xNQ1Bdn//KXTKwu5Wbu39XPRlBXc5VTiePAVttUH6EbYXZxsEp/0TI/4jLSp/ILF5UhVHE5lPFXVGsboe1vyB/LuAhsH3kcWUbLjaOhAQSWecO+hBud1qtQmTKXlU2+SWEPqgQ0VJmxHzrStDg5HFviek7D7yb9DY7lD2WBolZF6mJUpN5P5it8H3SDxmGCPbNC87Z0J4VQwx2VkPR3EM7Q7dmmMTfBpVTbLpBfllBxAX2jlRmV0dDPSzp8BKCyyE1e9kECBmR3HEzZTVebCQFiTE5bM6Hs02ixRGX/9h8xd2O87mmhAKnzhLfncSzHrqy54jwz+IWwBoJExdYX3yRbnZW4rewPxGdug98+lqYPuWDDrdvoTp80tPXujO/r3AaRC12leLKFyZE6vJ1Gp43FNYmpnEFrVCki1UEW4QqTCNk4A9osIT04i/pDjkIhMfJNWMGGVwddz3gQhQnaprcPJlehzSPhoJP/vjgfmS6bUOc5L5OSosFQOMFgZIVLvE7jZxKnudr5wU4tTQzJtVGL/U0usYr31MrvdqHX3STT+Do+tonigQYcC6AdVb2BXww8jKVBCd5E+R66jMxp+3w0eBdZKW1rmBal8kc6fOyiLEla0/83F5+NijwXJ+ssWYWHu2xQ4zaFNZYjFeqXkbxl8AYBeek1BREBJ16fXezlyYL4NLCm2ixugkFW7fSj3U2s7Qilvxtc6X9QQsOvZq2PShGWJL79NCBDsatjeWoR40x+GfrHCacwQFvvT45Ci7z+UYvGgA7qJUdP1Sm+La/aUJhi12iSqiHfhRgQu2SPw0IFCv4uqyJDCaX0aJPvCXR3MqbcEMtY7pnbkoALvq1eNhQMQ4J+zpWVo6ARl+BgB0236MQQ0yTYV5arEpZ9Cla+SNSmdMTL5kwHw/6yhDTa3CD2tjqpyBsvcvQjtPhSCL/Jvqg9ShSZkbwQ4EgZwTnhPJL1DAL3vPJ5ehkyNKL8iaZ06HYAvJYY1h72+adpsMHzYt/irTOOHKMeaMBrA1Z2QLtnEF+hXNa0Bi2pr8YK72fjMNBZREwS7pp1PqDKuP4spxc4knmWTeCLf119B3pD+7BjPZafKh+F3wPedDjomUERAXVThuhrIjELsC6pt0EvUqyyV7kBbttLtGJjj1qDR6TM5IzKHCEttawzMJfozlCYyEOuXaOubhx4JKYw+KBGlGwDm+uOsEHByUBKHW2RQqS5wBst9wam0koDIizntjg0jOLyHWD/GuZOsLMSAJ6sdaidbraXSHrf1jPkLdRHd3iZp9Vx83CWqkrDU24Pjc72r9VEKZ3TeDANFGxjk+25RGwX2fIj6XDL0Yzc0cNqjl8kAiY1jYUD9dieIOdCm9/L7VzYLBrQhJPZTsgmb3SfvmmFs1auQoJntvk998k33sDOcpCPRign2N0RNvrlVdqGAzq9G+iqobaFznruTsodpBeP3wWLHgdMTyl+wwtLwiQ6mL4r7lARTIi/p+NE1xkSh6HoJS6RtqWOAV+NtS7iEemQOxW3qTRL0RZO5c+aQKXDciOdhGqfsRPGGskMaUZTFbpUpyUB4di/P3sOrvgB3NNLh8g+uSonBxG5XjO/vH/hik7G9a2B95IaWnFt/TKLof0tKlByUjmkW1caqG7zjziKD1532VZuORz0F6AkNN97emjqXhxfBqndSyPGr/upXydB3bGUIZPSD7RvvXidVYziCPt6OsG3vBJJvb8JMQfxe+fYORxMQPcmDQ2GUhme4SPwf2VMfDqlr1QM6ZaESWeJAv6o0mNkq/8vThfV35yE3Oi4bR0+tI1WKCFT53fw5IIcUjR/v8D9iamW0mPOfpciSdbcuuMgLNW7+TNB2MOMFcOMouXjGk5nYa59lXHwT/npJYNq6fgHvPrfas2nNhAt9ajvnKr2P1Vbw0SXDJPRf5mG2erXau2AiE8YrXUZ9SfpNDcsU4B/ETOXa52sIL4a/P7fB3T5fDoPFoy7kMqwqPV7gTcAzNAcPrxR2OqNEUjGjyXsyfoeENI3+TNQ3dqFUGZSREng1DnfROTxR+9kuM7P5xkQjGUq2JY2ovcqUGzb1tGpC/ZSsIUBmFJfdcgoac3Mk1LXgCfLw5G/N6oHrjhud9ElkjHuq++WjzaFzGu/xXgVWE/DMuVJivjZGxE0sxnX7cvPK2muC3oaNTBltuKEaOnHHqHt9QMQMcY1oUmSVoHrvu2E4YQYBDer32dRFfaJIqCtJbpZ/thQpgBID4d4MgiyWI7e///gM6Ll5d')))).decode('utf-8'))